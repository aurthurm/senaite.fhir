# -*- coding: utf-8 -*-

from senaite.core.api import dtime
from senaite.fhir.datatype.meta import Meta
from senaite.fhir.interfaces import IFHIRResource
from zope.interface import implementer

_marker = object()


@implementer(IFHIRResource)
class FHIRResource(dict):

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

    def _get(self, data_type, name, as_list=False, default=None):
        value = self.get(name, _marker)
        if value is _marker:
            return default
        if as_list:
            return [data_type(record) for record in value]
        return data_type(value)
