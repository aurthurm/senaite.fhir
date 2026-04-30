# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.fhir import api as fapi
from senaite.fhir.r5 import add_route
from senaite.jsonapi import api

ENDPOINT_GET = "senaite.fhir.r5.get"

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
    uuids = list(filter(lambda val: fapi.is_uuid(val), [uid, resource_type]))
    if uuids:
        uuid = fapi.get_uuid(uuids[0])
        obj = api.get_object_by_uid(uuid.hex, default=None)
        if not obj:
            # XXX search brains by FHIR UID instead
            fapi.fail(msg="Not Found", status=404)
        fhir_resource = fapi.to_fhir_resource(obj)
        return fhir_resource.to_dict()

    # all resources from the defined type
    portal_type = api.resource_to_portal_type(resource_type)
    if portal_type is None:
        fapi.fail(msg="Not Found", status=404)

    return api.get_batched(portal_type=portal_type, uid=uid,
                           endpoint=ENDPOINT_GET)
