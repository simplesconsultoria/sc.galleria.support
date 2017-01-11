# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from sc.galleria.support.config import PROJECTNAME
from sc.galleria.support.testing import INTEGRATION_TESTING

import unittest2 as unittest


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IGalleriaLayer' in layers,
                        'browser layer not installed')

    def test_view_methods(self):
        types = self.portal['portal_types']
        galleria_view = 'galleria_view'
        self.assertIn(galleria_view, types['Collection'].view_methods)
        self.assertIn(galleria_view, types['Folder'].view_methods)
        self.assertIn(galleria_view, types['Link'].view_methods)
        self.assertIn(galleria_view, types['Topic'].view_methods)

    def test_upgrade_javascript_registry(self):
        portal_javascripts = self.portal.portal_javascripts
        resources = portal_javascripts.getResourceIds()
        self.assertTrue('++resource++collective.galleria.js' in resources)
        qi = self.portal.portal_quickinstaller
        setup = self.portal.portal_setup
        portal_javascripts.manage_removeScript('++resource++collective.galleria.js')
        setup.setLastVersionForProfile(u'sc.galleria.support:default', '1001')
        qi.upgradeProduct('sc.galleria.support')
        self.assertTrue('++resource++collective.galleria.js' in resources)


class UninstallTestCase(unittest.TestCase):

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

    def test_view_methods(self):
        types = self.portal['portal_types']
        galleria_view = 'galleria_view'
        self.assertNotIn(galleria_view, types['Collection'].view_methods)
        self.assertNotIn(galleria_view, types['Folder'].view_methods)
        self.assertNotIn(galleria_view, types['Link'].view_methods)
        self.assertNotIn(galleria_view, types['Topic'].view_methods)
