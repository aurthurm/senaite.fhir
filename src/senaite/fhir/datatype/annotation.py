# -*- coding: utf-8 -*-

from senaite.core.api import dtime
from senaite.fhir.datatype.element import Element


class Annotation(Element):
    """A text note which also contains information about who made the statement
    and when.
    https://hl7.org/fhir/R5/datatypes.html#Annotation
    """

    @property
    def text(self):
        """The text of the annotation in markdown format.
        https://hl7.org/fhir/R5/datatypes-definitions.html#Annotation.text
        """
        return self["text"]

    @property
    def time(self):
        """Indicates when this particular annotation was made.
        """
        return dtime.to_dt(self.get("time"))
