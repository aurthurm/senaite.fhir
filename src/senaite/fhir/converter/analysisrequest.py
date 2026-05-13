# -*- coding: utf-8 -*-

from senaite.fhir.interfaces import IFHIRToContent
from senaite.fhir.interfaces import IServiceRequestResource
from zope.component import adapter
from zope.interface import implementer


@adapter(IServiceRequestResource)
@implementer(IFHIRToContent)
class ResourceToAnalysisRequest(object):

    def __init__(self, resource):
        self.resource = resource

    def to_content_dict(self):
        # TODO We don't validate category + SNOMED code (is necessary?)

        # get the specimen
        specimen = self.get_specimen()
        if not specimen:
            raise ValueError("%r: Specimen is missing" % self.resource)

    def get_specimen(self):
        return None
