# -*- coding: utf-8 -*-
from senaite.fhir.datatype.code import Code
from senaite.fhir.resource import Resource

_marker = object()

class OperationOutcome(Resource):

    @property
    def severity(self):
        return self._get(Code, name="severity")

    @property
    def code(self):
        return self._get(Code, name="code")

    @property
    def details(self):
        # TODO CodeableConcept
        return self.get("details")

    @property
    def diagnostics(self):
        return self._get(str, name="diagnostics")

    @property
    def expression(self):
        return self._get(str, name="expression", as_list=True)
