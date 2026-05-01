# -*- coding: utf-8 -*-

class Meta(dict):
    """Metadata about a FHIR resource
    """

    @property
    def versionId(self):
        """The version specific identifier, as it appears in the version
        portion of the URL. This value changes when the resource is created,
        updated, or deleted.

        The server assigns this value, and ignores what the client specifies,
        except in the case that the server is imposing version integrity on
        updates/deletes.

        https://hl7.org/fhir/R5/resource-definitions.html#Meta.versionId
        """
        return self.get("versionId")

    @property
    def lastUpdated(self):
        """When the resource last changed - e.g. when the version changed.

        This element is generally omitted in instances submitted in a PUT or
        POST. Instead, it is populated in the response instance and when
        retrieving information using a GET. The server / resource manager
        sets this value; what a client provides is irrelevant. This is
        equivalent to the HTTP Last-Modified and SHOULD have the same value on
        a read interaction.

        https://hl7.org/fhir/R5/resource-definitions.html#Meta.lastUpdated
        """
        return self.get("lastUpdated")

    @property
    def source(self):
        """A uri that identifies the source system of the resource. This
        provides a minimal amount of Provenance information that can be used
        to track or differentiate the source of information in the resource.
        The source may identify another FHIR server, document, message,
        database, etc.

        The exact use of the source (and the possible implied
        Provenance.entity.role and agent.role) is left to implementer
        discretion. Only one nominated source is allowed; for additional
        provenance details, a full Provenance resource should be used. The
        source may correspond to Provenance.entity.what[x] or
        Provenance.agent.who[x], though it may be a more general or abstract
        reference.

        This element can be used to indicate where the current master source
        of a resource that has a canonical URL if the resource is no longer
        hosted at the canonical URL.

        https://hl7.org/fhir/R5/resource-definitions.html#Meta.source
        """
        return self.get("source")
