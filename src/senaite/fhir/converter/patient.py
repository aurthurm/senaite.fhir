# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.api import dtime
from senaite.fhir import api as fapi
from senaite.fhir.config import FHIR_PROFILE_URL
from senaite.fhir.interfaces import IFHIRConverter
from senaite.fhir.resource.patient import PatientResource
from senaite.patient.interfaces import IPatient
from zope.component import adapter
from zope.interface import implementer


@adapter(IPatient)
@implementer(IFHIRConverter)
class PatientToFHIRConverter(object):

    def __init__(self, context):
        self.context = context

    def to_fhir_id(self, system_id, value, use=None):
        if not value:
            return None
        data = {
            "system": "%s/Identifier/%s" % (FHIR_PROFILE_URL, system_id),
            "value": value,
        }
        if use:
            data["use"] = use
        return data

    def get_fhir_identifiers(self):
        # basic identifiers
        patient = self.context
        identifiers = [
            self.to_fhir_id("context", patient.getId(), use="usual"),
            self.to_fhir_id("mrn", patient.getMRN(), use="official")
        ]
        # secondary identifiers
        for key, value in patient.get_identifier_items():
            sys_id = fapi.slugify(key)
            fhir_id = self.to_fhir_id(sys_id, value, use="secondary")
            identifiers.append(fhir_id)
        # remove empties
        return list(filter(None, identifiers))

    def to_fhir_resource(self):
        patient = self.context
        modified = api.get_modification_date(patient)
        modified = dtime.to_localized_time(modified, long_format=True)
        uuid = fapi.get_uuid(patient)
        profile_url = "{}/StructureDefinition/Patient".format(FHIR_PROFILE_URL)
        data = {
            "resourceType": "Patient",
            "id": str(uuid),
            "status": api.get_review_status(patient),
            "meta": {
                "profile": [ profile_url ],
                "lastUpdated": modified,
            },
            "identifier": self.get_fhir_identifiers(),
        }

        given_name = [patient.getFirstname(), patient.getMiddlename()]
        data["name"] = {
            "family": patient.getLastname(),
            "given": list(filter(None, given_name)),
            "use": "official",
        }
        dob = patient.getBirthdate()
        data["birthDate"] = dtime.date_to_string(dob)
        data["gender"] = patient.getGenderText()

        return PatientResource(data)
