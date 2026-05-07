# -*- coding: utf-8 -*-


class Element(dict):
    """Base definition for all elements in a resource
    """

    @property
    def id(self):
        return self.get("id")

    @property
    def extension(self):
        from senaite.fhir.datatype.extension import Extension  # noqa
        data = self.get("extension") or []
        return [Extension(item) for item in data]
