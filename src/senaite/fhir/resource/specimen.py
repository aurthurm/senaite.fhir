# -*- coding: utf-8 -*-

from senaite.core.api import dtime
from senaite.fhir import api as fapi
from senaite.fhir.converter import get_by_key
from senaite.fhir.datatype.codeableconcept import CodeableConcept
from senaite.fhir.interfaces import ISpecimenResource
from senaite.fhir.resource import FHIRResource
from zope.interface import implementer


@implementer(ISpecimenResource)
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

    @property
    def bodySite(self):
        data = self.collection.get("bodySite")
        concept = data.get("concept")
        return CodeableConcept(concept) if concept else None

    def get_code(self, system=None):
        """Returns the code for the given system. If no system is set, uses
        the default system
        """
        if not system:
            system = fapi.get_system_code("Specimen")
        return get_by_key(self.type.coding, key="system", value=system)
