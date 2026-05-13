# -*- coding: utf-8 -*-

from senaite.fhir.datatype.backboneelement import BackboneElement
from senaite.fhir.datatype.codeableconcept import CodeableConcept


class OrderDetailParameter(BackboneElement):
    """"
    The parameter details for the service being requested
    https://fhir.senaite.org/StructureDefinition-SenaiteServiceRequest-definitions.html#key_ServiceRequest.orderDetail.parameter
    """
    @property
    def code(self):
        """A value representing the additional detail or instructions for the
        order (e.g., catheter insertion, body elevation, descriptive device
        configuration and/or setting instructions).
        https://fhir.senaite.org/StructureDefinition-SenaiteServiceRequest-definitions.html#key_ServiceRequest.orderDetail.parameter.code
        """
        return CodeableConcept(self.get("code"))

    @property
    def valueCodeableConcept(self):
        """Indicates a value for the order detail.
        https://fhir.senaite.org/StructureDefinition-SenaiteServiceRequest-definitions.html#key_ServiceRequest.orderDetail.parameter.value[x]
        """
        return CodeableConcept(self.get("valueCodeableConcept"))
