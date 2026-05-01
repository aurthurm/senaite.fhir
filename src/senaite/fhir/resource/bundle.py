# -*- coding: utf-8 -*-

from senaite.fhir.resource import Resource
from senaite.fhir.resource.operationoutcome import OperationOutcome


class Bundle(Resource):

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
