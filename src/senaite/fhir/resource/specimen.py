# -*- coding: utf-8 -*-

from senaite.core.api import dtime
from senaite.fhir.datatype.codeableconcept import CodeableConcept
from senaite.fhir.resource import FHIRResource

_marker = object()


class SpecimenResource(FHIRResource):

    @property
    def type(self):
        data = self.get("type")
        return CodeableConcept(data) if data else data

    @property
    def collection(self):
        return self.get("collection")

    @property
    def collectedDateTime(self):
        data = self.collection or {}
        return dtime.to_dt(data.get("collectedDateTime"))
