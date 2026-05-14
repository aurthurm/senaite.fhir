# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.catalog import SETUP_CATALOG
from senaite.fhir.converter.analysisrequest import PRIORITIES
from senaite.fhir.interfaces import IFHIRToContent
from senaite.fhir.interfaces import ISpecimenResource
from zope.component import adapter
from zope.interface import implementer


@adapter(ISpecimenResource)
@implementer(IFHIRToContent)
class ResourceToAnalysisRequest(object):

    def __init__(self, resource):
        self.resource = resource

    def to_content_dict(self):
        # TODO We don't validate category + SNOMED code (is necessary?)

        sample_type = self.get_sample_type()
        client = self.get_client()
        contact = self.get_requester()
        specs = self.get_specifications_for(sample_type)
        sample_point = self.get_sample_point()
        date_sampled = self.get_date_sampled()
        profiles = self.get_profiles()
        services = self.get_services()
        priority = self.get_priority()

        data = {
            "Client": client,
            "Contact": contact,
            "SampleType": sample_type,
            "SamplePoint": sample_point,
            "DateSampled": date_sampled,
            "Profiles": profiles,
            "Priority": priority,
            # "Sampler": collector,
            # "Remarks": remarks,
            "Specification": specs,
            "Services": services,
        }

        # update with patient information
        patient_info = self.get_patient_info()
        data.update(patient_info)
        return data

    def get_reference_obj(self, key):
        ref = getattr(self.resource, key, None)
        if not ref:
            raise ValueError("%r: %s is missing" % (self.resource, key))

        if api.is_list(ref):
            if len(ref) > 1:
                raise ValueError("%r: More than one %s" % (self.resource, key))
            ref = ref[0]

        # get the uid
        uid = ref.UID()
        if not uid:
            raise ValueError("%r: Not a valid %s ref", (self.resource, key))

        # search by uid
        obj = api.get_object_by_uid(uid, default=None)
        if not obj:
            raise ValueError("%r: No %s found: %s", (self.resource, key, uid))

        return obj

    def get_sample_type(self):
        """Returns the SampleType object associated to this ServiceRequest
        """
        return self.get_reference_obj("specimen")

    def get_requester(self):
        """Returns the contact who requested the sample
        """
        return self.get_reference_obj("requester")

    def get_patient(self):
        """Returns the patient assigned to this ServiceRequest
        """
        return self.get_reference_obj("subject")

    def get_client(self):
        """Returns the client the sample where the sample has to be created
        """
        return self.get_reference_obj("client")

    def get_specifications_for(self, sample_type):
        """Returns the analysis specification that is associated to the
        given sample type
        """
        query = {
            "portal_type": "AnalysisSpec",
            "sampletype_uid": api.get_uid(sample_type),
            "is_active": True,
        }
        # TODO What to do when more than one spec per sample type?
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])
        return None

    def get_date_sampled(self):
        """Returns the date when the specimen was collected
        """
        # TODO see Bundle.specimen.collection.collectedDateTime
        return None

    def get_sample_point(self):
        """Returns the sample point from where this specimen was collected
        """
        # TODO see Bundle.specimen.collection.bodySite
        return None

    def get_services(self):
        """Returns the list of services to assign to this sample
        """
        # TODO Fix empty list
        return []

    def get_profiles(self):
        """Returns a list of analysis profiles
        """
        # TODO Fix empty list
        return []

    def get_priority(self):
        """Returns the priority
        """
        #  routine | urgent | asap | stat
        priority = self.resource.priority
        return dict(PRIORITIES).get(priority, "5")

    def get_patient_info(self):
        patient = self.get_patient()
        patient_mrn = patient.getMRN()
        patient_dob = patient.getBirthdate()
        patient_sex = patient.getSex()
        return {
            "PatientFullName": {
                "firstname": patient.getFirstname(),
                "middlename": patient.getMiddlename(),
                "lastname": patient.getLastname(),
            },
            "DateOfBirth": patient_dob,
            "Sex": patient_sex,
            "MedicalRecordNumber": {"value": patient_mrn}
        }
