# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from sc.galleria.support.config import PROJECTNAME
from sc.galleria.support.interfaces import IFlickrPlugin
from sc.galleria.support.interfaces import IGeneralSettings
from sc.galleria.support.interfaces import IHistoryPlugin
from sc.galleria.support.interfaces import IPicasaPlugin
from sc.galleria.support.interfaces import IFaceBookPlugin
from sc.galleria.support.testing import INTEGRATION_TESTING


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
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

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('galleria' in actions,
                        'control panel was not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('galleria' not in actions,
                        'control panel was not removed')


class RecordsGeneralSettings(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IGeneralSettings)

    def test_autoplay_record(self):
        self.assertTrue(hasattr(self.settings, 'autoplay'))
        self.assertEqual(self.settings.autoplay, True)

    def test_showInf_record(self):
        self.assertTrue(hasattr(self.settings, 'showInf'))
        self.assertEqual(self.settings.showInf, True)

    def test_gallery_width_record(self):
        self.assertTrue(hasattr(self.settings, 'gallery_width'))
        self.assertEqual(self.settings.gallery_width, 500)

    def test_gallery_height_record(self):
        self.assertTrue(hasattr(self.settings, 'gallery_height'))
        self.assertEqual(self.settings.gallery_height, 500)

    def test_imagePosition_record(self):
        self.assertTrue(hasattr(self.settings, 'imagePosition'))
        self.assertEqual(self.settings.imagePosition, u'center')

    def test_lightbox_record(self):
        self.assertTrue(hasattr(self.settings, 'lightbox'))
        self.assertEqual(self.settings.lightbox, False)

    def test_showCounting_record(self):
        self.assertTrue(hasattr(self.settings, 'showCounting'))
        self.assertEqual(self.settings.showCounting, True)

    def test_transitions_record(self):
        self.assertTrue(hasattr(self.settings, 'transitions'))
        self.assertEqual(self.settings.transitions, u'fade')

    def test_transitionSpeed_record(self):
        self.assertTrue(hasattr(self.settings, 'transitionSpeed'))
        self.assertEqual(self.settings.transitionSpeed, 400)

    def test_showimagenav_record(self):
        self.assertTrue(hasattr(self.settings, 'showimagenav'))
        self.assertEqual(self.settings.showimagenav, True)

    def test_swipe_record(self):
        self.assertTrue(hasattr(self.settings, 'swipe'))
        self.assertEqual(self.settings.swipe, True)

    def test_selector_record(self):
        self.assertTrue(hasattr(self.settings, 'selector'))
        self.assertEqual(self.settings.selector, u"#content-galleria")

    def test_thumbnails_record(self):
        self.assertTrue(hasattr(self.settings, 'thumbnails'))
        self.assertEqual(self.settings.thumbnails, u'show')

    def test_imagecrop_record(self):
        self.assertTrue(hasattr(self.settings, 'imagecrop'))
        self.assertEqual(self.settings.imagecrop, True)

    def test_responsive_record(self):
        self.assertTrue(hasattr(self.settings, 'responsive'))
        self.assertEqual(self.settings.responsive, True)

    def test_debug_record(self):
        self.assertTrue(hasattr(self.settings, 'debug'))
        self.assertEqual(self.settings.debug, False)


class RecordsFlickrPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IFlickrPlugin)

    def test_flickr_record(self):
        self.assertTrue(hasattr(self.settings, 'flickr'))
        self.assertEqual(self.settings.flickr, False)

    def test_flickr_max_record(self):
        self.assertTrue(hasattr(self.settings, 'flickr_max'))
        self.assertEqual(self.settings.flickr_max, 20)

    def test_flickr_desc_record(self):
        self.assertTrue(hasattr(self.settings, 'flickr_desc'))
        self.assertEqual(self.settings.flickr_desc, False)


class RecordsPicasaPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IPicasaPlugin)

    def test_picasa_record(self):
        self.assertTrue(hasattr(self.settings, 'picasa'))
        self.assertEqual(self.settings.picasa, False)

    def test_picasa_max_record(self):
        self.assertTrue(hasattr(self.settings, 'picasa_max'))
        self.assertEqual(self.settings.picasa_max, 20)

    def test_picasa_desc_record(self):
        self.assertTrue(hasattr(self.settings, 'picasa_desc'))
        self.assertEqual(self.settings.picasa_desc, False)


class RecordsFaceBookPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IFaceBookPlugin)

    def test_facebook_record(self):
        self.assertTrue(hasattr(self.settings, 'facebook'))
        self.assertEqual(self.settings.facebook, False)

    def test_facebook_max_record(self):
        self.assertTrue(hasattr(self.settings, 'facebook_max'))
        self.assertEqual(self.settings.facebook_max, 20)

    def test_facebook_desc_record(self):
        self.assertTrue(hasattr(self.settings, 'facebook_desc'))
        self.assertEqual(self.settings.facebook_desc, False)


class RecordsHistoryPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IHistoryPlugin)

    def test_history_record(self):
        self.assertTrue(hasattr(self.settings, 'history'))
        self.assertEqual(self.settings.history, False)
