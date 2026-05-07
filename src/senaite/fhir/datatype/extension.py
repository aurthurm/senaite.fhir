# -*- coding: utf-8 -*-

class Extension(dict):
    """Object that represents an Extension datatype
    https://hl7.org/fhir/R5/extensibility.html#Extension
    """

    @property
    def url(self):
        return self.get("url")
