# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

from sc.galleria.support.testing import INTEGRATION_TESTING


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='galleria-settings')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                          '@@galleria-settings')

    def test_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('galleria' in actions)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
