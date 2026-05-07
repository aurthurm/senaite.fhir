# -*- coding: utf-8 -*-
import collections

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


def get_by_key(items, key, value, default=None):
    items = items if items else []
    for item in items:
        if item.get(key) == value:
            return item
    return default

def group_by(items, key):
    groups = collections.OrderedDict()
    items = items if items else []
    for item in items:
        val = item.get(key)
        groups.setdefault(val, []).append(item)
    return groups
