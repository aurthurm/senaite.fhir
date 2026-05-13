# -*- coding: utf-8 -*-

from senaite.fhir.datatype.element import Element
from senaite.fhir import api as fapi


class Reference(Element):
    """The Reference type contains at least one of a reference (literal
    reference), an identifier (logical reference), and a display (text
    description of target). In addition, it may contain a target type.
    https://hl7.org/fhir/R5/references.html#Reference
    """

    @property
    def reference(self):
        """Literal reference, Relative, internal or absolute URL
        https://hl7.org/fhir/R5/references-definitions.html#Reference.reference
        """
        return self.get("reference")

    @property
    def type(self):
        """Type the reference refers to (e.g. "Patient") - must be a resource
        in resources.
        https://hl7.org/fhir/R5/references-definitions.html#Reference.type
        Value set at https://hl7.org/fhir/R5/valueset-resource-types.html
        """
        return self.get("type")

    def UID(self):
        """Handy accessor that returns the UID hex form of the reference
        Mimics the default behavior of AT/DX
        """
        if not self.reference:
            return None
        # remove the resource type, if any
        raw_id = self.reference.split("/")[-1]
        try:
            uuid = fapi.get_uuid(raw_id)
        except (TypeError, ValueError):
            return None
        return uuid.hex
