# -*- coding: utf-8 -*-

import transaction

from bika.lims import api
from senaite.core.api import dtime
from senaite.fhir import api as fapi
from senaite.fhir.converter import to_fhir_profile_url
from senaite.fhir.interfaces import IBundleResource
from senaite.fhir.r5 import add_route
from senaite.fhir.resource.bundleresponse import BundleResponseResource
from senaite.jsonapi import api as japi
from senaite.jsonapi import request as req

ENDPOINT = "senaite.fhir.r5"
ENDPOINT_GET = "%s.get" % ENDPOINT
ENDPOINT_POST = "%s.post" % ENDPOINT


# /<resource_type>
@add_route("/<string:resource_type>",
           ENDPOINT_GET, methods=["GET"])
@add_route("/<string:resource_type>/<string(length=32):uid>",
           ENDPOINT_GET, methods=["GET"])
@add_route("/<string(length=32):uid>",
           ENDPOINT_GET, methods=["GET"])
@add_route("/<string:resource_type>/<string(length=36):uid>",
           ENDPOINT_GET, methods=["GET"])
@add_route("/<string(length=36):uid>",
           ENDPOINT_GET, methods=["GET"])
def get(context, request, resource_type=None, uid=None):
    """GET
    """
    # maybe we received a request by uid/uuid
    uuids = list(filter(lambda val: fapi.is_uuid(val), [uid, resource_type]))
    if uuids:
        uid = fapi.get_uuid(uuids[0]).hex
        return fapi.to_fhir_resource(uid)

    # all resources from the defined type
    portal_type = japi.resource_to_portal_type(resource_type)
    if portal_type is None:
        fapi.fail(msg="Not Found", status=404)

    # TODO Return a FHIR batch of resources?
    return japi.get_batched(portal_type=portal_type, uid=uid,
                            endpoint=ENDPOINT_GET)


@add_route("/<string:resource_type>", ENDPOINT_POST, methods=["POST"])
def post(context, request, resource_type=None):
    # disable CSRF
    req.disable_csrf_protection()

    # get the FHIR resources from the request
    resources = get_fhir_resources()

    entries = []
    errored = False
    for resource in resources:

        # Skip if creation or update of this resource is not supported
        if not fapi.can_create_or_update(resource):
            continue

        # create or update the counterpart object
        obj = fapi.get_object(resource, default=None)
        if not errored:
            try:
                if not obj:
                    obj = fapi.create(resource)
                    status = "201 Created"
                else:
                    obj = fapi.update(resource)
                    status = "201 Updated"
            except Exception as e:
                errored = True
                status = "500 %s" % str(e)
                # prevent partial commits
                transaction.abort()
        else:
            status = "500 Skipped due to a previous error"

        # build the response entry
        fullUrl = "%s/%s" % (resource.resourceType, resource.id)
        modified = api.get_modification_date(obj) if obj else dtime.now()
        modified = dtime.to_iso_format(modified)

        # set up the basics of the response entry for this item
        entry = {
            "fullUrl": fullUrl,
            "response": {
                "status": status,
                "lastModified": modified,
            }
        }
        entries.append(entry)

    # create the BundleResponse
    resp = {
        "resourceType": "Bundle",
        "id": str(fapi.generate_UUID()),
        "meta": {
            "profile": [to_fhir_profile_url("SenaiteBundleResponse")]
        },
        "type": "transaction-response",
        "entry": entries,
    }
    return BundleResponseResource(resp)


def get_fhir_resources():
    """Returns the resources from the request
    """
    resources = []

    # get the FHIR raw records
    records = req.get_request_data()
    for record in records:
        # convert to a FHIR resource
        resource = fapi.to_fhir_resource(record)

        # if the resource is a Bundle, extract all contained resources
        if IBundleResource.providedBy(resource):
            for entry in resource.entry:
                # convert each entry to a FHIR resource
                entry_res = fapi.to_fhir_resource(entry)
                if not entry_res:
                    continue
                # assign the bundle so we can resolve references
                # TODO this '_bundle' dance is a bit ugly
                entry_res["_bundle"] = resource
                # add to the resources list
                resources.append(entry_res)

        # append the resource
        resources.append(resource)

    return resources
