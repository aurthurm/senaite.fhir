# -*- coding: utf-8 -*-
import copy

from senaite.core.api import dtime
from senaite.fhir.converter import first_by
from senaite.fhir.converter import get_by_key
from senaite.fhir.datatype.extension import Extension
from senaite.fhir.datatype.meta import Meta
from senaite.fhir.interfaces import IFHIRResource
from zope.interface import implementer

_marker = object()


@implementer(IFHIRResource)
class FHIRResource(dict):

    def __init__(self, seq=None, **kwargs):
        super(FHIRResource, self).__init__(seq, **kwargs)
        self._validate()

    @property
    def resourceType(self):
        """Returns the resource type
        """
        return self.get("resourceType")

    @property
    def id(self):
        """Returns the logical id of the artifact
        https://hl7.org/fhir/R5/resource.html#id
        """
        return self.get("id")

    @property
    def meta(self):
        """Returns the metadata about the resource
        """
        data = self.get("meta") or {}
        return Meta(data)

    @property
    def implicitRules(self):
        """A set of rules under which this content was created
        """
        return self.get("implicitRules") or []

    @property
    def language(self):
        """Language of the resource content
        """
        return self.get("language")

    @property
    def modified(self):
        """Returns the last modification date of this resource
        Mimics te behaviour of DX and AT types
        """
        return dtime.to_dt(self.meta.lastUpdated)

    @property
    def extension(self):
        """Returns a list of Extension data types, if any
        """
        data = self.get("extension") or []
        return [Extension(item) for item in data]

    def get_extension(self, url):
        """Returns an Extension of this resource by url, if any
        """
        return get_by_key(self.extension, key="url", value=url)

    def get_external_id(self):
        """Returns the Identifier object representing the identifier
        originating from the API's consumer system (e.g. the ordering EHR or
        middleware)
        https://fhir.senaite.org/identifiers.html
        """
        # TODO Move this function to fapi.resource
        identifiers = getattr(self, "identifier", [])
        return first_by(identifiers, use="secondary")

    def get_object_id(self):
        """Returns the Identifier object representing the internal identifier
        created and assigned by SENAITE
        https://fhir.senaite.org/identifiers.html
        """
        # TODO Move this function to fapi.resource
        identifiers = getattr(self, "identifier", [])
        return first_by(identifiers, use="usual")

    def to_dict(self):
        return copy.deepcopy(dict(self))

    def _get(self, data_type, name, as_list=False, default=None):
        value = self.get(name, _marker)
        if value is _marker:
            return default
        if as_list:
            return [data_type(record) for record in value]
        return data_type(value)

    def _validate(self):
        """Looks through all properties and validates any constraint
        """
        # TODO Implement (loop through attr and use decorators for constraints)
        pass

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.id or "--no-id--")

    def __repr__(self):
        return self.__str__()
