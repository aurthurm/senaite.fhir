# -*- coding: utf-8 -*-
from senaite.fhir.datatype.period import Period

SALUTATIONS = ("dr", "mr", "ms", "mx")


class HumanName(dict):
    """Object that represents an HL7 HumanName datatype
    https://www.hl7.org/fhir/datatypes.html#humanname
    """

    @property
    def use(self):
        return self.get("use")

    @property
    def text(self):
        return self.get("text")

    @property
    def family(self):
        return self.get("family")

    @property
    def given(self):
        return self.get("given") or []

    @property
    def prefix(self):
        return self.get("prefix") or []

    @property
    def suffix(self):
        return self.get("suffix") or []

    @property
    def period(self):
        data = self.get("period")
        if data:
            return Period(data)
        return None

    def get_name_info(self):
        """Returns a dict with the name parts
        """
        info = {
            "Salutation": "",
            "Firstname": "",
            "Middleinitial": "",
            "Middlename": "",
            "Surname": "",
        }

        family = self.family
        given = self.given
        prefix = self.prefix
        if all([family, given]):
            info.update({
                "Salutation": prefix[0] if prefix else "",
                "Firstname": given[0],
                "Surname": family,
                "Middlename": " ".join(given[1:]),
            })
            return info

        # Rely on the 'text' entry
        fullname = self.get("text")
        parts = filter(None, fullname.split(" "))
        if not parts:
            return info

        if len(parts) == 1:
            info["Firstname"] = parts[0]
            return info

        if parts[0].strip(".").lower() in SALUTATIONS:
            info["Salutation"] = parts[0]
            parts = parts[1:]

        info["Firstname"] = parts[0]
        info["Surname"] = " ".join(parts[1:])
        return info
