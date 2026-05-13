# -*- coding: utf-8 -*-

from senaite.fhir.interfaces import IFHIRToContent
from senaite.fhir.interfaces import IServiceRequestResource
from zope.component import adapter
from zope.interface import implementer
from bika.lims import api


@adapter(IServiceRequestResource)
@implementer(IFHIRToContent)
class ResourceToAnalysisRequest(object):

    def __init__(self, resource):
        self.resource = resource

    def to_content_dict(self):
        # TODO We don't validate category + SNOMED code (is necessary?)
        # get the sample_type
        sample_type = self.get_sample_type()

        # get the practitioner who requested the sample
        requester = self.get_requester()

        # get the client
        client = self.get_client()

        # get the services
        services = self.get_services()
        services = [api.get_uid(service) for service in services]

        return {
            "SampleType": api.get_uid(sample_type),
            "Contact": api.get_uid(requester),
            "Client": api.get_uid(client),
            "Services": [services],
        }

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

    def get_client(self):
        """Returns the client the sample where the sample has to be created
        """
        return self.get_reference_obj("client")

    def get_services(self):
        """Returns the list of services to assign to this sample
        """
        return []
