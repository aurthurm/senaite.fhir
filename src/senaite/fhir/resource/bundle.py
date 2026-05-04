# -*- coding: utf-8 -*-

from senaite.fhir.api import to_fhir_resource
from senaite.fhir.resource import FHIRResource
from senaite.fhir.resource.operationoutcome import OperationOutcome


class Bundle(FHIRResource):

    @property
    def type(self):
        return self.get("type")

    @property
    def issues(self):
        """Captures issues and warnings that relate to the construction of the
        Bundle and the content within it.
        """
        records = self.get("issues") or []
        return [OperationOutcome(record) for record in records]

    @property
    def entry(self):
        entries = self.get("entry") or []
        resources = []
        for entry in entries:
            # TODO fullUrl (e.g. urn:uuid:ddaf107d-a44d-4b7b-966b-65d82de495cc)
            full_url = entry.get("fullUrl")
            raw_resource = entry.get("resource")

            # TODO Only interested on resuorces that resolve to our own FHIRResource
            resource = to_fhir_resource(raw_resource, default=None)
            if resource:
                resources.append(resource)

        return resources
