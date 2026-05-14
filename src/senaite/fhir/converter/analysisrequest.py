# -*- coding: utf-8 -*-
from senaite.fhir.converter import first_by
from senaite.fhir.interfaces import IFHIRToContent
from senaite.fhir.interfaces import IServiceRequestResource
from zope.component import adapter
from zope.interface import implementer
from bika.lims import api
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.catalog import CONTACT_CATALOG
from senaite.fhir import api as fapi
from plone.memoize.instance import memoize


# Priorities mapping
PRIORITIES = (
    ("stat", "1"),
    ("asap", "2"),
    ("urgent", "3"),
    ("routine", "5"),
)


@adapter(IServiceRequestResource)
@implementer(IFHIRToContent)
class ResourceToAnalysisRequest(object):

    def __init__(self, resource):
        self.resource = resource

    def to_content_dict(self):
        # TODO We don't validate category + SNOMED code (is necessary?)

        sample_type = self.get_sample_type()
        client = self.get_client()
        contact = self.get_requester()
        specs = self.get_specifications()
        sample_point = self.get_sample_point()
        date_sampled = self.get_date_sampled()
        profiles = self.get_profiles()
        services = self.get_services()
        priority = self.get_priority()

        data = {
            "portal_type": "AnalysisRequest",
            "parent_path": api.get_path(client),
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
            "Analyses": services,
        }

        # update with patient information
        patient_info = self.get_patient_info()
        data.update(patient_info)
        return data

    def get_reference(self, key):
        ref = getattr(self.resource, key, None)
        if not ref:
            raise ValueError("%r: %s is missing" % (self.resource, key))
        if api.is_list(ref):
            if len(ref) > 1:
                raise ValueError("%r: More than one %s" % (self.resource, key))
            return ref[0]
        return ref

    def get_reference_obj(self, key, **kwargs):
        ref = self.get_reference(key)
        uid = ref.UID()
        return api.get_object_by_uid(uid, default=None)

    def get_bundle_sibling(self, ref):
        bundle = self.resource.get("_bundle")
        if not bundle:
            return None
        return bundle.first_entry("id", str(ref.UUID()))

    @memoize
    def get_sample_type(self):
        """Returns the SampleType object associated to this ServiceRequest
        """
        # Try with the reference UID first
        ref = self.get_reference("specimen")
        uid = ref.UID()
        obj = fapi.get_object(uid, default=None)
        if obj:
            return obj

        # get the sibling from the bundle, if any
        sibling = self.get_bundle_sibling(ref)
        if not sibling:
            raise ValueError("%r: No SampleType for specimen: %s" %
                             (self.resource, uid))

        # search by code / title
        # TODO Consider to add a search function in fapi and use adapters
        # TODO Add a field to SampleType (SNOMED code) to search by code
        code = sibling.get_code()
        display = code.display.lower()
        # use sortable_title for an ignore case search
        query = dict(portal_type="SampleType", sortable_title=display.lower())
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])

        raise ValueError("%r: No SampleType for specimen: %s" %
                         (self.resource, uid))

    @memoize
    def get_requester(self):
        """Returns the contact who requested the sample
        """
        # Try with the reference UID first
        ref = self.get_reference("requester")
        uid = ref.UID()
        obj = fapi.get_object(uid, default=None)
        if obj:
            return obj

        # get the sibling from the bundle, if any
        sibling = self.get_bundle_sibling(ref)
        if not sibling:
            raise ValueError("%r: No Client for %s" % (self.resource, uid))

        # TODO Consider to add a search function in fapi and use adapters
        # search by practitioner ID (use=secondary)
        contact_id = sibling.get_external_id()
        if contact_id:
            # TODO New field External ID in contact to search by
            query = dict(portal_type="Contact", getExternalID=contact_id)
            # brains = api.search(query, CONTACT_CATALOG)
            brains = []
            if len(brains) == 1:
                return api.get_object(brains[0])

        # fallback to search by fullname (from the client)
        client = self.get_client()
        fullname = sibling.get_fullname()
        if client and fullname:
            fullname = sibling.get_fullname()
            query = {
                "portal_type": "Contact",
                "getFullname": fullname,
                "path": {
                    "query": "/".join(client.getPhysicalPath()),
                    "level": 0
                }
            }
            brains = api.search(query, CONTACT_CATALOG)
            if len(brains) == 1:
                return api.get_object(brains[0])

        raise ValueError("%r: No Contact for %s" % (self.resource, uid))

    @memoize
    def get_patient(self):
        """Returns the patient assigned to this ServiceRequest
        """
        # Try with the reference UID first
        ref = self.get_reference("subject")
        uid = ref.UID()
        obj = fapi.get_object(uid, default=None)
        if obj:
            return obj

        raise ValueError("%r: No Patient for %s" % (self.resource, uid))

    @memoize
    def get_client(self):
        """Returns the client the sample where the sample has to be created
        """
        # try with the reference first
        ref = self.resource.client
        uid = ref.UID()
        obj = fapi.get_object(uid, default=None)
        if obj:
            return obj

        # get the sibling from the bundle, if any
        sibling = self.get_bundle_sibling(ref)
        if not sibling:
            raise ValueError("%r: No Client for %s" % (self.resource, uid))

        # TODO Consider to add a search function in fapi and use adapters
        # search by client ID (use=secondary)
        client_id = sibling.get_external_id()
        if client_id:
            query = dict(portal_type="Client", getClientID=client_id)
            brains = api.search(query, SETUP_CATALOG)
            if len(brains) == 1:
                return api.get_object(brains[0])

        # fallback to search by title (ignorecase)
        query = dict(portal_type="Client", sortable_title=sibling.name)
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])

        raise ValueError("%r: No Client for %s" % (self.resource, uid))

    @memoize
    def get_specifications(self):
        """Returns the analysis specification for this sample
        """
        sample_type = self.get_sample_type()
        if not sample_type:
            return None

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

    @memoize
    def get_date_sampled(self):
        """Returns the date when the specimen was collected
        """
        ref = self.get_reference("specimen")
        specimen = self.get_bundle_sibling(ref)
        return specimen.collectedDateTime

    @memoize
    def get_sample_point(self):
        """Returns the sample point from where this specimen was collected
        """
        ref = self.get_reference("specimen")
        specimen = self.get_bundle_sibling(ref)
        if not specimen:
            return None

        # get the bodySite coding element
        if not specimen.bodySite:
            return None

        system = fapi.get_system_code("SamplePoint")
        site = first_by(specimen.bodySite.coding, system=system)
        if not site:
            return None

        # TODO Consider to add a search function in fapi and use adapters
        external_id = site.code
        if external_id:
            # TODO New field External ID in SamplePoint to search by
            query = dict(portal_type="SamplePoint", getExternalID=site.code)
            # brains = api.search(query, SETUP_CATALOG)
            brains = []
            if len(brains) == 1:
                return api.get_object(brains[0])

        # fallback to search by title
        display = site.display
        if display:
            # use sortable_title for an ignore case search
            title = display.lower()
            query = dict(portal_type="SamplePoint", sortable_title=title)
            brains = api.search(query, SETUP_CATALOG)
            if len(brains) == 1:
                return api.get_object(brains[0])

        return None

    def get_services(self):
        """Returns the list of services to assign to this sample
        """
        # TODO Fix empty list
        return []

    def get_profiles(self):
        """Returns a list of analysis profiles
        """
        self.resource.code.concept
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
