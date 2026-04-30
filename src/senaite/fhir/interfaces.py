# -*- coding: utf-8 -*-


from zope.interface import Interface



class IFHIRResource(Interface):
    """Marker interface for a FHIR's HL7 resource
    """

    def UID(self):
        """Returns the UID of this resource
        """


class IFHIRConverter(Interface):
    """Converter of AT/DX content to/from IFHIRResource
    """


class IFHIRContent(Interface):
    """Marker interface for objects that has a linked FHIR Resource
    """
