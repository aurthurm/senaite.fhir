# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.api import dtime
from senaite.fhir.datatype.humanname import HumanName
from senaite.fhir.datatype.identifier import Identifier
from senaite.fhir.resource import FHIRResource
from senaite.patient.config import GENDERS

_marker = object()


class PatientResource(FHIRResource):

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

    @property
    def gender(self):
        return self.get("gender")

    @property
    def birthDate(self):
        return dtime.to_dt(self.get("birthDate"))

    def get_mrn(self):
        identifier = self.get_identifier("usual")
        if not identifier:
            return ""
        return identifier.get("value", "")

    def get_identifier(self, use):
        for identifier in self.get("identifier"):
            if identifier.get("use") == use:
                return identifier
        return None

    def get_fullname(self):
        """Get patient's full name from resource payload
        """
        patient_names = self.get("name")
        fullname = next((
            name for name in patient_names
            if name.get("use") == "official"
        ), None)
        return fullname

    def get_givenname(self):
        """Get patient's given name from full name
        """
        fullname = self.get_fullname()
        if fullname:
            return fullname.get("given", "")
        return ""

    def get_address(self):
        """Get patient's address from resource payload
        """
        patient_addresses = self.get("address")
        if not patient_addresses:
            return None
        address = next((
            patient_address for patient_address in patient_addresses
            if patient_address.get("type") == "physical"
               and patient_address.get("use") == "home"  # noqa
        ), None)
        return address

    def to_object_info(self):
        """Returns a dict representation of the Patient resource, suitable for
        the creation and edition of SENAITE Patient objects
        """
        sexes = dict(GENDERS)
        mrn = self.get_mrn()
        sex = sexes.get(self.get("gender")) or ""
        fullname = self.get_fullname()
        # If no "official" name found, use the first available name
        if not fullname:
            patient_names = self.get("name")
            if patient_names:
                fullname = patient_names[0]

        givenname = self.get_givenname()
        firstname = givenname[0] if givenname != "" else ""
        middlename = (
            givenname[1]
            if givenname != "" and len(givenname) == 2 else ""
        )
        lastname = fullname.get("family", "") if fullname else ""
        birthdate = self.get("birthDate")
        address = self.get_address()

        if address:
            address_line = address.get("line", [""])
            address = list([{
                "type": api.safe_unicode(address.get("type", "")),
                "address": (
                    api.safe_unicode(address_line[0]) if address_line else ""
                ),
                "city": api.safe_unicode(address.get("city", "")),
            }])

        return {
            "mrn": mrn,
            "sex": sex,
            "birthdate": birthdate,
            "address": address,
            "gender": "",
            "firstname": api.safe_unicode(firstname),
            "middlename": api.safe_unicode(middlename),
            "lastname": api.safe_unicode(lastname),
            "portal_type": "Patient",
        }
