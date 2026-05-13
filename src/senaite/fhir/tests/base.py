# -*- coding: utf-8 -*-

import transaction
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.testing import zope
from senaite.core.tests.base import BaseTestCase
from senaite.core.tests.layers import BaseLayer


class SimpleTestLayer(BaseLayer):

    def setUpZope(self, app, configurationContext):
        super(SimpleTestLayer, self).setUpZope(app, configurationContext)

        # Load ZCML
        import senaite.fhir
        import senaite.patient

        # Load ZCML
        self.loadZCML(package=senaite.patient)
        self.loadZCML(package=senaite.fhir)

        # Install product and call its initialize() function
        zope.installProduct(app, "senaite.patient")
        zope.installProduct(app, "senaite.fhir")

    def setUpPloneSite(self, portal):
        super(SimpleTestLayer, self).setUpPloneSite(portal)
        applyProfile(portal, "senaite.fhir:default")
        transaction.commit()


SIMPLE_TEST_LAYER_FIXTURE = SimpleTestLayer()
SIMPLE_TESTING = FunctionalTesting(
    bases=(SIMPLE_TEST_LAYER_FIXTURE,),
    name="senaite.fhir:SimpleTesting"
)


class SimpleTestCase(BaseTestCase):
    """Use for test cases which do not rely on demo data
    """
    layer = SIMPLE_TESTING

    def setUp(self):
        super(SimpleTestCase, self).setUp()
