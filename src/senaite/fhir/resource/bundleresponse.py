# -*- coding: utf-8 -*-

from senaite.fhir.interfaces import IServiceRequestBundleResource
from senaite.fhir.resource.bundle import Bundle
from senaite.fhir.resource.operationoutcome import OperationOutcome
from zope.interface import implementer


@implementer(IServiceRequestBundleResource)
class BundleResponseResource(Bundle):
    """The transaction-response Bundle returned by the server after
    successfully processing a SenaiteRequestBundle. One entry is returned per
    entry in the request, in the same order. Each entry carries the
    server-assigned fullUrl and a response status. No resource body or request
    element is included.
    https://fhir.senaite.org/StructureDefinition-SenaiteBundleResponse.html
    """

    __cardinality = (
        ("id", "1..1"),
        ("identifier", "0..1"),
        ("total", "0..0"),
        ("type", "1..1"),
        ("timestamp", "0..1"),
        ("total", "0..0"),
        ("link", "0..0"),
        ("entry", "1..*"),
        ("signature", "0..0"),
        ("issues", "0..1"),
    )

    __fixed_values = (
        ("type", "transaction-response"),
    )

    @property
    def id(self):
        """Returns the logical id of the artifact
        https://fhir.senaite.org/StructureDefinition-SenaiteBundleResponse-definitions.html#key_Bundle.id
        """
        return self["id"]

    @property
    def implicitRules(self):
        """A set of rules under which this content was created
        https://fhir.senaite.org/StructureDefinition-SenaiteBundleResponse-definitions.html#key_Bundle.implicitRules
        """
        return self.get("implicitRules") or []

    @property
    def type(self):
        """Indicates the purpose of this bundle, how it is intended to be used.
        Fixed Value: transaction-response
                     https://hl7.org/fhir/valueset-bundle-type.html
        https://fhir.senaite.org/StructureDefinition-SenaiteBundleResponse-definitions.html#key_Bundle.type
        """
        return self["type"]

    @property
    def issues(self):
        """Captures issues and warnings that relate to the construction of the
        Bundle and the content within it.
        https://fhir.senaite.org/StructureDefinition-SenaiteBundleResponse-definitions.html#Bundle.issues
        """
        records = self.get("issues") or []
        return [OperationOutcome(record) for record in records]

    @property
    def entry(self):
        """An entry in a bundle resource - will either contain a resource or
        information about a resource (transactions and history only).
        https://fhir.senaite.org/StructureDefinition-SenaiteBundleResponse-definitions.html#Bundle.entry
        """
        return super(BundleResponseResource, self).entry
