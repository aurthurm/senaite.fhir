# -*- coding: utf-8 -*-
from senaite.fhir.datatype.element import Element
from senaite.fhir.datatype.period import Period


class ContactPoint(Element):
    """Object that represents a ContactPoint datatype
    https://hl7.org/fhir/R5/datatypes-definitions.html#ContactPoint
    """

    @property
    def system(self):
        """Telecommunications form for contact point.
        Value set: phone | fax | email | pager | url | sms | other
        https://hl7.org/fhir/R5/valueset-contact-point-system.html
        """
        return self.get("system")

    @property
    def value(self):
        return self.get("value")

    @property
    def use(self):
        """Use of contact point.
        Value set: home | work | temp | old | mobile
        https://hl7.org/fhir/R5/valueset-contact-point-use.html
        """
        return self.get("use")

    @property
    def rank(self):
        return self.get("rank")

    @property
    def period(self):
        data = self.get("period")
        return Period(data) if data else None
