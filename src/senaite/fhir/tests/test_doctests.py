# -*- coding: utf-8 -*-

import doctest
from os.path import join

import unittest2 as unittest
from pkg_resources import resource_listdir
from Testing import ZopeTestCase as ztc

from senaite.fhir import PRODUCT_NAME
from senaite.fhir.tests.base import SimpleTestCase

# Option flags for doctests
flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF


def test_suite():
    suite = unittest.TestSuite()
    for doctest_file in get_doctest_files():
        suite.addTests([
            ztc.ZopeDocFileSuite(
                doctest_file,
                test_class=SimpleTestCase,
                optionflags=flags
            )
        ])
    return suite


def get_doctest_files():
    """
    Return the available doctest files for this package.
    """
    files = resource_listdir(PRODUCT_NAME, "tests/doctests")
    files = filter(lambda name: name.endswith(".rst"), files)
    return map(lambda name: join("doctests", name), files)
