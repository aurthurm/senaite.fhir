# -*- coding: utf-8 -*-

from senaite.core.api import dtime


class Period(dict):

    @property
    def start(self):
        return dtime.to_dt(self.get("start"))

    @property
    def end(self):
        return dtime.to_dt(self.get("end"))
