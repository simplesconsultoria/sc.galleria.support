# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from sc.galleria.support.config import PROJECTNAME
from sc.galleria.support.testing import INTEGRATION_TESTING

JS = [
    '++resource++galleria-scripts/galleria-1.2.6.min.js',
    ]


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_dependencies_installed(self):
        packages = ['plone.app.registry']
        for p in packages:
            self.assertTrue(self.qi.isProductInstalled(p),
                            '%s not installed' % p)

    def test_browserlayer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IGalleriaLayer' in layers,
                        'browser layer not installed')

    def test_javascript_registry(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JS:
            self.assertTrue(js in portal_javascripts.getResourceIds())


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('IGalleriaLayer' in layers,
                         'browser layer not removed')

    def test_javascript_registry_removed(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JS:
            self.assertTrue(js not in portal_javascripts.getResourceIds())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
