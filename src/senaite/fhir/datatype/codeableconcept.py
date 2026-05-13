# -*- coding: utf-8 -*-

from senaite.fhir.datatype.coding import Coding


class CodeableConcept(dict):
    """A CodeableConcept represents a value that is usually supplied by
    providing a reference to one or more terminologies or ontologies but may
    also be defined by the provision of text. This is a common pattern in
    healthcare data.
    https://hl7.org/fhir/R5/datatypes.html#CodeableConcept
    """

    @property
    def coding(self):
        """A reference to a code defined by a terminology system.
        https://hl7.org/fhir/R5/datatypes-definitions.html#CodeableConcept.coding
        """
        items = self.get("coding") or []
        return [Coding(item) for item in items]

    @property
    def text(self):
        """Plain text representation of the concept
        https://hl7.org/fhir/R5/datatypes-definitions.html#CodeableConcept.text
        """
        return self.get("text")
