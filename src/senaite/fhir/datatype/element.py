# -*- coding: utf-8 -*-


class Element(dict):
    """Base definition for all elements in a resource
    """

    @property
    def id(self):
        """Unique id for inter-element referencing
        """
        return self.get("id")

    @property
    def extension(self):
        """Additional content defined by implementations
        """
        from senaite.fhir.datatype.extension import Extension  # noqa
        data = self.get("extension") or []
        return [Extension(item) for item in data]
