# -*- coding: utf-8 -*-

import logging

from .browser import router

PRODUCT_NAME = "senaite.fhir"
FHIR_CURRENT_VERSION = "r5"
DEFAULT_ROUTE = "senaite.fhir.get"

logger = logging.getLogger(PRODUCT_NAME)


def add_route(route, endpoint=None, fhir_version=FHIR_CURRENT_VERSION, **kw):
    """Add a new FHIR API route
    """
    # slashes cleanup
    route = '/'.join(s.strip('/') for s in ["", fhir_version, route])
    def wrapper(f):
        try:
            router.DefaultFHIRRouter.add_url_rule(route,
                                                  endpoint=endpoint,
                                                  view_func=f,
                                                  options=kw)
        except AssertionError, e:
            logger.warn("Failed to register route {}: {}".format(route, e))
        return f
    return wrapper


def url_for(endpoint, **values):
    """Looks up the FHIR URL for the given endpoint

    :param endpoint: The name of the registered route (aka endpoint)
    :type endpoint: string
    :returns: External URL for this endpoint
    :rtype: string/None
    """
    return router.DefaultFHIRRouter.url_for(endpoint, force_external=True,
                                            values=values)
