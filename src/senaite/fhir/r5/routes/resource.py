# -*- coding: utf-8 -*-

from senaite.fhir.r5 import add_route
from senaite.jsonapi import api
from senaite.jsonapi.exceptions import APIError

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
def get(context, request, resource_type=None, uid=None):
    """GET
    """
    # We have a UID, return the record
    if uid and not resource_type:
        return api.get_record(uid)

    # we have a UID as the resource type, return the FHIR resource
    if api.is_uid(resource_type):
        return api.get_record(resource_type)

    portal_type = api.resource_to_portal_type(resource_type)
    if portal_type is None:
        raise APIError(404, "Not Found")

    return api.get_batched(portal_type=portal_type, uid=uid,
                           endpoint=ENDPOINT_GET)
