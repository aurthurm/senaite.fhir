# -*- coding: utf-8 -*-

import re
from uuid import UUID

from bika.lims import api
from persistent.dict import PersistentDict
from senaite.fhir import logger
from senaite.fhir.config import FHIR_STORAGE_KEY
from senaite.fhir.exceptions import FHIRAPIError
from senaite.fhir.interfaces import IContentToFHIR
from senaite.fhir.interfaces import IFHIRContent
from senaite.fhir.interfaces import IFHIRResource
from senaite.fhir.interfaces import IFHIRToContent
from zope.annotation.interfaces import IAnnotations
from zope.component import queryAdapter
from zope.interface import alsoProvides

_marker = object()


def fail(msg, status=500):
    """API Error
    """
    if msg is None:
        msg = "Reason not given."
    raise FHIRAPIError(status, "{}".format(msg))


def is_fhir_content(obj):
    """Returns whether the object passed in was created from a FHIR resource
    """
    return IFHIRContent.providedBy(obj)


def is_fhir_resource(obj):
    """Returns whether the thing is a FHIR Resource object
    """
    return IFHIRResource.providedBy(obj)


def get_fhir_storage(obj):
    """Get or creates the FHIR annotation storage for the given object

    :param obj: Content object
    :returns: PersistentDict
    """
    annotation = IAnnotations(obj)
    if annotation.get(FHIR_STORAGE_KEY) is None:
        annotation[FHIR_STORAGE_KEY] = PersistentDict()
    return annotation[FHIR_STORAGE_KEY]

def is_uuid(thing):
    try:
        get_uuid(thing)
        return True
    except (TypeError, ValueError):
        return False

def get_uuid(thing):
    """Returns the UUID object
    """
    if isinstance(thing, UUID):
        return thing
    if is_fhir_resource(thing):
        return UUID(thing.id)
    if api.is_object(thing):
        return UUID(api.get_uid(thing))
    return UUID(thing)


def get_uid(obj):
    """Returns the UUID in hex format
    """
    if is_fhir_resource(obj):
        return get_uuid(obj).hex
    return api.get_uid(obj)


def get_fhir_uid(obj):
    """Returns the UID of the counterpart FHIR content, if any
    """
    if is_fhir_resource(obj):
        return get_uid(obj)
    obj = api.get_object(obj)
    if is_fhir_content(obj):
        storage = get_fhir_storage(obj)
        return storage.get("uid", None)
    return None


def get_object(thing, default=_marker):
    if is_fhir_resource(thing):
        thing = get_uid(thing)
    if default is _marker:
        return api.get_object(thing)
    return api.get_object(thing, default=default)


def to_fhir_resource(thing, default=_marker):
    """Converts the object to a FHIR resource
    """
    if not thing:
        return None

    if is_fhir_resource(thing):
        return thing

    if isinstance(thing, dict):
        rtype = thing.get("resourceType")
        if not rtype:
            if default is _marker:
                fail(msg="Not well formed resource. Resource type is missing")
            return default

        # Look for FHIRResource named adapters (wrappers)
        resource = queryAdapter(thing, IFHIRResource, rtype)
        if not resource:
            if default is _marker:
                fail(msg="Resource type is not supported: %s" % rtype)
            return default

        return resource

    if api.is_uid(thing):
        thing = api.get_object_by_uid(thing, default=None)
        if not thing:
            if default is _marker:
                fail(msg="Not Found", status=404)
            return default

    obj = api.get_object(thing)
    adapter = queryAdapter(obj, IContentToFHIR)
    if not adapter:
        if default is _marker:
            fail(msg="Type is not supported: %r" % obj)
        return default

    return adapter.to_fhir_resource()


def create(resource):
    """Creates a counterpart object for the given FHIR Resource
    """
    if not is_fhir_resource(resource):
        raise ValueError("Type not supported: {}".format(repr(type(resource))))

    # check if already exists
    uid = get_uid(resource)
    obj = api.get_object_by_uid(uid, default=None)
    if obj:
        raise ValueError("Object with UID '%s' exists: %r" % (uid, obj))

    # create the underlying entries/dependencies first
    objects = []
    entries = getattr(resource, "entry", [])
    for entry in entries:
        obj = get_object(entry, default=None)
        if not obj:
            # TODO rely on a setting to whether create or not
            # create if it does not exist
            obj = create(entry)

        if obj:
            objects.append(obj)

    # convert the resource to a content dict
    adapter = queryAdapter(resource, IFHIRToContent)
    if not adapter:
        logger.warn("Cannot create content for FHIR '%s' resource type. No "
                    "IFHIRToContent adapter found" % resource.resourceType)
        return None

    data = adapter.to_content_dict()
    if not data:
        return None

    # create the object
    portal_type = data.pop("portal_type")
    container = data.pop("parent_path")
    container = api.get_object(container)
    return api.create(container, portal_type, **data)


def link_fhir_resource(obj, resource):
    """Assigns a FHIR  resource to the given obj
    """
    if not is_fhir_resource(resource):
        raise ValueError("Type not supported: {}".format(repr(type(resource))))

    # mark the object with IFHIRContent, so we can always know beforehand if
    # this object has a counterpart FHIR resource
    alsoProvides(obj, IFHIRContent)

    # assign the FHIR UID, along with current data so we can always use the
    # original information, even when connection with source is lost
    annotation = get_fhir_storage(obj)
    annotation["uid"] = get_uid(resource)
    annotation["data"] = resource.to_dict()


def slugify(value, repl="-"):
    repl = repl if repl else ""
    slug = value.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", repl, slug)
    slug = re.sub(r"^-+|-+$", "", slug)
    return slug
