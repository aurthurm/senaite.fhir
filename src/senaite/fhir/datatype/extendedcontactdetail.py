# -*- coding: utf-8 -*-

from senaite.fhir.datatype.address import Address
from senaite.fhir.datatype.contactpoint import ContactPoint
from senaite.fhir.datatype.element import Element
from senaite.fhir.datatype.humanname import HumanName
from senaite.fhir.datatype.period import Period


class ExtendedContactDetail(Element):
    """Object that represents an ExtendedContactDetail metadata type
    https://hl7.org/fhir/R5/metadatatypes.html#ExtendedContactDetail
    """

    @property
    def purpose(self):
        """The type of contact
        https://terminology.hl7.org/5.1.0/ValueSet-contactentity-type.html
        """
        return self.get("purpose")

    @property
    def name(self):
        """Name of an individual to contact
        https://hl7.org/fhir/R5/datatypes.html#HumanName
        """
        data = self.get("name")
        return HumanName(data) if data else None

    @property
    def telecom(self):
        """Contact details (e.g.phone/fax/url)
        https://hl7.org/fhir/R5/datatypes.html#ContactPoint
        """
        data = self.get("telecom") or []
        return [ContactPoint(item) for item in data]

    @property
    def address(self):
        """Address for the contact
        https://hl7.org/fhir/R5/datatypes.html#Address
        """
        data = self.get("address")
        return Address(data) if data else None

    @property
    def organization(self):
        """This contact detail is handled/monitored by a specific organization
        https://hl7.org/fhir/R5/organization.html
        """
        from senaite.fhir.resource.organization import OrganizationResource
        data = self.get("organization")
        return OrganizationResource(data)

    @property
    def period(self):
        """Period that this contact was valid for usage
        https://hl7.org/fhir/R5/datatypes.html#Period
        """
        data = self.get("period")
        return Period(data) if data else None
