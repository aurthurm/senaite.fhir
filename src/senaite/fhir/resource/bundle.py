# -*- coding: utf-8 -*-

from senaite.fhir.api import to_fhir_resource
from senaite.fhir.interfaces import IBundleResource
from senaite.fhir.resource import FHIRResource
from senaite.fhir.resource.operationoutcome import OperationOutcome
from zope.interface import implementer


@implementer(IBundleResource)
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
            # full_url = entry.get("fullUrl")
            raw_resource = entry.get("resource")

            # TODO Only interested on resources resolving to our FHIRResource
            resource = to_fhir_resource(raw_resource, default=None)
            if resource:
                resources.append(resource)

        # TODO Sorting of entries from inside a Bundle is not neat
        # sort the entries so they are processed in the right order
        order = ["Organization", "Practitioner", "Patient"]
        return sorted(
            resources,
            key=lambda en: order.index(en.resourceType)
            if en.resourceType in order else len(order)
        )
