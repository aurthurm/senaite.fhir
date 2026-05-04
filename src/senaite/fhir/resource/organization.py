# -*- coding: utf-8 -*-

from senaite.fhir.resource import FHIRResource


class OrganizationResource(FHIRResource):

    @property
    def active(self):
        return self.get("active", True)

    @property
    def name(self):
        return self.get("name")
