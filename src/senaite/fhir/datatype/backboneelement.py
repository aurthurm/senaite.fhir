# -*- coding: utf-8 -*-

from senaite.fhir.datatype.element import Element


class BackboneElement(Element):
    """The base definition for complex elements defined as part of a resource
    definition - that is, elements that have children that are defined in the
    resource.
    """

    @property
    def modifierExtension(self):
        """Extensions that cannot be ignored even if unrecognized
        """
        from senaite.fhir.datatype.extension import Extension  # noqa
        data = self.get("modifierExtension") or []
        return [Extension(item) for item in data]
