# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from sc.galleria.support.testing import INTEGRATION_TESTING


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)

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


class RecordsGeneralSettings(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)

    def test_record_autoplay(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_autoplay = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.autoplay']
        self.failUnless('autoplay' in IGeneralSettings)
        self.assertEquals(record_autoplay.value, True)

    def test_record_showInf(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_showInf = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.showInf']
        self.failUnless('showInf' in IGeneralSettings)
        self.assertEquals(record_showInf.value, True)

    def test_record_gallery_width(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_gallery_width = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.gallery_width']
        self.failUnless('gallery_width' in IGeneralSettings)
        self.assertEquals(record_gallery_width.value, 500)

    def test_record_gallery_height(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_gallery_height = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.gallery_height']
        self.failUnless('gallery_height' in IGeneralSettings)
        self.assertEquals(record_gallery_height.value, 500)

    def test_record_imagePosition(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_imagePosition = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.imagePosition']
        self.failUnless('imagePosition' in IGeneralSettings)
        self.assertEquals(record_imagePosition.value, u'center')

    def test_record_lightbox(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_lightbox = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.lightbox']
        self.failUnless('lightbox' in IGeneralSettings)
        self.assertEquals(record_lightbox.value, False)

    def test_record_showCounting(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_showCounting = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.showCounting']
        self.failUnless('showCounting' in IGeneralSettings)
        self.assertEquals(record_showCounting.value, True)

    def test_record_transitions(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_transitions = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.transitions']
        self.failUnless('transitions' in IGeneralSettings)
        self.assertEquals(record_transitions.value, u'fade')

    def test_record_transitionSpeed(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_transitionSpeed = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.transitionSpeed']
        self.failUnless('transitionSpeed' in IGeneralSettings)
        self.assertEquals(record_transitionSpeed.value, 400)

    def test_record_showimagenav(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_showimagenav = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.showimagenav']
        self.failUnless('showimagenav' in IGeneralSettings)
        self.assertEquals(record_showimagenav.value, True)

    def test_record_swipe(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_swipe = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.swipe']
        self.failUnless('swipe' in IGeneralSettings)
        self.assertEquals(record_swipe.value, True)

    def test_record_selector(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_selector = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.selector']
        self.failUnless('selector' in IGeneralSettings)
        self.assertEquals(record_selector.value, u"#content")

    def test_record_thumbnails(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_thumbnails = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.thumbnails']
        self.failUnless('thumbnails' in IGeneralSettings)
        self.assertEquals(record_thumbnails.value, u'show')

    def test_record_debug(self):
        from sc.galleria.support.interfaces import IGeneralSettings
        record_debug = self.registry.records[
            'sc.galleria.support.interfaces.IGeneralSettings.debug']
        self.failUnless('debug' in IGeneralSettings)
        self.assertEquals(record_debug.value, False)


class RecordsFlickrPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)

    def test_record_flickr(self):
        from sc.galleria.support.interfaces import IFlickrPlugin
        record_flickr = self.registry.records[
            'sc.galleria.support.interfaces.IFlickrPlugin.flickr']
        self.failUnless('flickr' in IFlickrPlugin)
        self.assertEquals(record_flickr.value, False)

    def test_record_flickr_max(self):
        from sc.galleria.support.interfaces import IFlickrPlugin
        record_flickr_max = self.registry.records[
            'sc.galleria.support.interfaces.IFlickrPlugin.flickr_max']
        self.failUnless('flickr_max' in IFlickrPlugin)
        self.assertEquals(record_flickr_max.value, 20)

    def test_record_flickr_desc(self):
        from sc.galleria.support.interfaces import IFlickrPlugin
        record_flickr_desc = self.registry.records[
            'sc.galleria.support.interfaces.IFlickrPlugin.flickr_desc']
        self.failUnless('flickr_desc' in IFlickrPlugin)
        self.assertEquals(record_flickr_desc.value, False)


class RecordsPicasaPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)

    def test_record_picasa(self):
        from sc.galleria.support.interfaces import IPicasaPlugin
        record_picasa = self.registry.records[
            'sc.galleria.support.interfaces.IPicasaPlugin.picasa']
        self.failUnless('picasa' in IPicasaPlugin)
        self.assertEquals(record_picasa.value, False)

    def test_record_picasa_max(self):
        from sc.galleria.support.interfaces import IPicasaPlugin
        record_picasa_max = self.registry.records[
            'sc.galleria.support.interfaces.IPicasaPlugin.picasa_max']
        self.failUnless('picasa_max' in IPicasaPlugin)
        self.assertEquals(record_picasa_max.value, 20)

    def test_record_picasa_desc(self):
        from sc.galleria.support.interfaces import IPicasaPlugin
        record_picasa_desc = self.registry.records[
            'sc.galleria.support.interfaces.IPicasaPlugin.picasa_desc']
        self.failUnless('picasa_desc' in IPicasaPlugin)
        self.assertEquals(record_picasa_desc.value, False)


class RecordsHistoryPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)

    def test_record_history(self):
        from sc.galleria.support.interfaces import IHistoryPlugin
        record_history = self.registry.records[
            'sc.galleria.support.interfaces.IHistoryPlugin.history']
        self.failUnless('history' in IHistoryPlugin)
        self.assertEquals(record_history.value, False)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
