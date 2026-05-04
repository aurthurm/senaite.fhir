# -*- coding: utf-8 -*-

from senaite.fhir.datatype.humanname import HumanName
from senaite.fhir.datatype.identifier import Identifier
from senaite.fhir.resource import FHIRResource

_marker = object()


class PractitionerResource(FHIRResource):

    @property
    def name(self):
        items = self.get("name") or []
        return [HumanName(item) for item in items]

    @property
    def identifier(self):
        """Returns the Identifier that identifies the organization across
        multiple systems
        """
        data = self.get("identifier") or []
        return [Identifier(item) for item in data]
