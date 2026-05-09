# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.fhir.converter.person import ResourceToPerson
from senaite.fhir.interfaces import IFHIRToContent
from senaite.fhir.interfaces import IPractitionerResource
from zope.component import adapter
from zope.interface import implementer


@adapter(IPractitionerResource)
@implementer(IFHIRToContent)
class ResourceToContact(ResourceToPerson):

    def get_parent(self):
        """Returns the parent object to which the counterpart object should
        belong to
        """
        # TODO this 'siblings' dance is a bit ugly
        siblings = self.resource.get("siblings")
        parent_uid = siblings.get("Organization")
        return api.get_object_by_uid(parent_uid, default=None)

    def to_content_dict(self):
        # contact should belong to a client (Organization)
        parent = self.get_parent()
        if not parent:
            raise ValueError("%r: Cannot infer parent" % self.resource)

        # build the dict
        data = super(ResourceToContact, self).to_content_dict()
        data.update({
            "portal_type": "Contact",
            "parent_path": api.get_path(parent),
        })
        return data
