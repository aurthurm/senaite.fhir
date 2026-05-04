# -*- coding: utf-8 -*-

from senaite.fhir.datatype.coding import Coding


class CodeableConcept(dict):
    """A CodeableConcept represents a value that is usually supplied by
    providing a reference to one or more terminologies or ontologies but may
    also be defined by the provision of text. This is a common pattern in
    healthcare data.
    """

    @property
    def coding(self):
        items = self.get("coding") or []
        return [Coding(item) for item in items]
