# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.api import dtime
from senaite.fhir import api as fapi
from senaite.fhir.converter import to_fhir_identifier as to_fhir_id
from senaite.fhir.converter import to_fhir_profile_url
from senaite.fhir.interfaces import IContentToFHIR
from senaite.fhir.interfaces import IFHIRToContent
from senaite.fhir.interfaces import IPatientResource
from senaite.fhir.resource.patient import PatientResource
from senaite.patient.interfaces import IPatient
from zope.component import adapter
from zope.interface import implementer


@adapter(IPatient)
@implementer(IContentToFHIR)
class PatientToResource(object):

    def __init__(self, patient):
        self.patient = patient

    def get_fhir_identifiers(self):
        # basic identifiers
        identifiers = [
            to_fhir_id("context", self.patient.getId(), use="usual"),
            to_fhir_id("mrn", self.patient.getMRN(), use="official")
        ]
        # secondary identifiers
        for key, value in self.patient.get_identifier_items():
            sys_id = fapi.slugify(key)
            fhir_id = to_fhir_id(sys_id, value, use="secondary")
            identifiers.append(fhir_id)
        # remove empties
        return list(filter(None, identifiers))

    def to_fhir_resource(self):
        modified = api.get_modification_date(self.patient)
        modified = dtime.to_localized_time(modified, long_format=True)
        uuid = fapi.get_uuid(self.patient)
        profile_url = to_fhir_profile_url("Patient")
        data = {
            "resourceType": "Patient",
            "id": str(uuid),
            "status": api.get_review_status(self.patient),
            "meta": {
                "profile": [ profile_url ],
                "lastUpdated": modified,
            },
            "identifier": self.get_fhir_identifiers(),
        }

        given = [self.patient.getFirstname(), self.patient.getMiddlename()]
        data["name"] = {
            "family": self.patient.getLastname(),
            "given": list(filter(None, given)),
            "use": "official",
        }
        dob = self.patient.getBirthdate()
        data["birthDate"] = dtime.date_to_string(dob)
        data["gender"] = self.patient.getGenderText()

        return PatientResource(data)


@adapter(IPatientResource)
@implementer(IFHIRToContent)
class ResourceToPatient(object):

    def __init__(self, resource):
        self.resource = resource

    def to_content_dict(self):
        return {}
