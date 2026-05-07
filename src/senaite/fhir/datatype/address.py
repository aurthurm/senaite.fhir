# -*- coding: utf-8 -*-
from senaite.fhir.datatype.period import Period


class Address(dict):
    """An address expressed using postal conventions (as opposed to GPS or
    other location definition formats). This datatype may be used to convey
    addresses for use in delivering mail as well as for visiting locations
    which might not be valid for mail delivery. There are a variety of postal
    address formats defined around the world.
    https://hl7.org/fhir/R5/datatypes.html#Address
    """

    @property
    def use(self):
        """Purpose of this address
        Value set: home | work | temp | old | billing
        https://hl7.org/fhir/R5/valueset-address-use.html
        """
        return self.get("use")

    @property
    def type(self):
        """Type of this address
        Value set: postal | physical | both
        https://hl7.org/fhir/R5/valueset-address-type.html
        """
        return self.get("type")

    @property
    def text(self):
        """Text representation of the address
        """
        return self.get("text")

    @property
    def line(self):
        """Street name, number, direction & P.O. Box etc.
        This repeating element order: The order in which lines should appear
        in an address label
        """
        return self.get("line") or []

    @property
    def city(self):
        """Name of city, town etc.
        """
        return self.get("city")

    @property
    def district(self):
        """District name (aka county)
        """
        return self.get("district")

    @property
    def state(self):
        """Sub-unit of country (abbreviations ok)
        """
        return self.get("state")

    @property
    def postalCode(self):
        """Postal code for area
        """
        return self.get("postalCode")

    @property
    def country(self):
        """Country (e.g. may be ISO 3166 2 or 3 letter code)
        """
        return self.get("country")

    @property
    def period(self):
        """Time period when address was/is in use
        """
        data = self.get("period")
        return Period(data) if data else None

    @property
    def url(self):
        return self.get("url")
