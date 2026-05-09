# -*- coding: utf-8 -*-
import copy

from bika.lims import api
from senaite.fhir import api as fapi
from senaite.fhir.interfaces import IBundleResource
from senaite.fhir.r5 import add_route
from senaite.jsonapi import api
from senaite.jsonapi import request as req

ENDPOINT = "senaite.fhir.r5"
ENDPOINT_GET = "%s.get" % ENDPOINT
ENDPOINT_POST = "%s.post" % ENDPOINT

# /<resource_type>
@add_route("/<string:resource_type>",
           ENDPOINT_GET, methods=["GET"])
#
# /<resource_type>/<uid>
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
    portal_type = api.resource_to_portal_type(resource_type)
    if portal_type is None:
        fapi.fail(msg="Not Found", status=404)

    # TODO Return a FHIR batch of resources?
    return api.get_batched(portal_type=portal_type, uid=uid,
                           endpoint=ENDPOINT_GET)


@add_route("/<string:resource_type>", ENDPOINT_POST, methods=["POST"])
def post(context, request, resource_type=None):
    # disable CSRF
    req.disable_csrf_protection()

    # get the FHIR resources from the request
    resources = get_fhir_resources()
    for resource in resources:
        # create or update the counterpart object
        obj = fapi.create_or_update(resource)

    # TODO Create and Return a Bundle Response
    # https://fhir.senaite.org/StructureDefinition-SenaiteBundleResponse.html
    return {}


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
            # build a dict of resourceType:uid to passthrough as siblings
            entries = resource.entry
            siblings = {en.resourceType:fapi.get_uid(en) for en in entries}
            for entry in entries:
                # convert each entry to a FHIR resource
                entry_res = fapi.to_fhir_resource(entry)
                if not entry_res:
                    continue
                # inject the siblings
                entry_res["siblings"] = copy.deepcopy(siblings)
                # add to the resources list
                resources.append(entry_res)

        # append the resource
        resources.append(resource)

    return resources
