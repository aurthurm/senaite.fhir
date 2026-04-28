# -*- coding: utf-8 -*-

import pkgutil

from senaite.fhir import add_route as add_fhir_route
from senaite.fhir import logger
from senaite.fhir.r5 import routes


def add_route(route, endpoint=None, **kw):
    """Add a new FHIR API route
    """
    return add_fhir_route(route, endpoint, fhir_version="r5", **kw)


prefix = routes.__name__ + "."
for importer, modname, ispkg in pkgutil.iter_modules(
        routes.__path__, prefix):
    module = __import__(modname, fromlist="dummy")
    logger.info("INITIALIZED SENAITE FHIR V1 ROUTE ---> %s" % module.__name__)
