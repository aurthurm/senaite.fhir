# -*- coding: utf-8 -*-

from senaite.fhir.config import FHIR_BASE_URL


def to_fhir_identifier(system_id, value, use=None):
    if not value:
        return None
    data = {
        "system": "%s/NamingSystem/%s" % (FHIR_BASE_URL, system_id),
        "value": value,
    }
    if use:
        data["use"] = use
    return data


def to_fhir_profile_url(resource_type):
    if not resource_type:
        return None
    return "%s/StructureDefinition/%s" % (FHIR_BASE_URL, resource_type)
