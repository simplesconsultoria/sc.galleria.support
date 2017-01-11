# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.galleria.support.config import PROJECTNAME
from sc.galleria.support.testing import INTEGRATION_TESTING

import unittest2 as unittest


class ContentTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_collection(self):
        self.portal.invokeFactory('Collection', 'test')
        obj = self.portal['test']
        obj.setLayout('galleria_view')
        self.assertEqual(obj.getLayout(), 'galleria_view')
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertEqual(obj.getLayout(), 'standard_view')

    def test_folder(self):
        self.portal.invokeFactory('Folder', 'test')
        obj = self.portal['test']
        obj.setLayout('galleria_view')
        self.assertEqual(obj.getLayout(), 'galleria_view')
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertEqual(obj.getLayout(), 'folder_listing')

    def test_link(self):
        self.portal.invokeFactory('Link', 'test')
        obj = self.portal['test']
        obj.setLayout('galleria_view')
        self.assertEqual(obj.getLayout(), 'galleria_view')
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertEqual(obj.getLayout(), 'link_redirect_view')
