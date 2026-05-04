# -*- coding: utf-8 -*-


class Coding(dict):
    """A Coding is a representation of a defined concept using a symbol from
    a defined "code system"
    """

    @property
    def system(self):
        return self.get("system")

    @property
    def version(self):
        return self.get("version")

    @property
    def code(self):
        return self.get("code")

    @property
    def display(self):
        return self.get("display")

    @property
    def userSelected(self):
        return self.get("userSelected")
