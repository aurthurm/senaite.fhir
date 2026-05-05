# -*- coding: utf-8 -*-


from zope.interface import Interface



class IFHIRResource(Interface):
    """Marker interface for a FHIR's resource
    """


class IPatientResource(IFHIRResource):
    """Marker interface for a FHIR's Patient resource
    """


class IContentToFHIR(Interface):
    """Converter of AT/DX content to IFHIRResource
    """

    def to_fhir_resource(self):
        """Returns the conversion of the context
        """


class IFHIRToContent(Interface):
    """Converter of IFHIRResource to AT/DX info dict
    """

    def to_content_dict(self):
        """Returns a dict suitable for the creation or update of a content
        type object
        """


class IFHIRContent(Interface):
    """Marker interface for objects that has a linked FHIR Resource
    """
