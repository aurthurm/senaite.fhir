# -*- coding: utf-8 -*-
from senaite.fhir.datatype.period import Period


class Identifier(dict):
    """An identifier intended for computation
    """

    @property
    def use(self):
        return self.get("use")

    @property
    def type(self):
        return self.get("type")

    @property
    def system(self):
        return self.get("system")

    @property
    def value(self):
        return self.get("value")

    @property
    def period(self):
        raw = self.get("period")
        return Period(raw) if raw else None

    @property
    def assigner(self):
        return self.get("assigner")
