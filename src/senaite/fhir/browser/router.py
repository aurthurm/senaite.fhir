# -*- coding: utf-8 -*-

from plone.jsonapi.core.browser.router import Router
from zope.globalrequest import getRequest


class FHIRRouter(Router):
    """FHIR API Router

    Mirrors plone.jsonapi.core's DefaultRouter but is dispatched only
    by the @@FHIR browser view, so FHIR routes stay isolated from the
    JSON API routes registered on plone.jsonapi.core.router.DefaultRouter.
    """

    view_name = "FHIR"

    def url_for(self, endpoint, **options):
        # Same logic as plone.jsonapi.core.browser.router.Router.url_for,
        # but breaks on this router's view name (FHIR / @@FHIR) instead
        # of the hardcoded API / @@API marker.
        request = getRequest()
        spp = request.physicalPathFromURL(self.url)

        path = []
        for el in spp:
            path.append(el)
            if el == self.view_name or el == "@@" + self.view_name:
                break

        virt_path = request.physicalPathToVirtualPath(path)
        script_name = request.physicalPathToURL(virt_path, relative=1)

        adapter = self.get_adapter(script_name=script_name)
        return adapter.build(endpoint, **options)


DefaultFHIRRouter = FHIRRouter()
