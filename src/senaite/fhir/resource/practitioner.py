# -*- coding: utf-8 -*-

from senaite.fhir.datatype.humanname import HumanName
from senaite.fhir.resource import FHIRResource

_marker = object()


class PractitionerResource(FHIRResource):

    @property
    def name(self):
        items = self.get("name") or []
        return [HumanName(item) for item in items]
