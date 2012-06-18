# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter

from Products.ATContentTypes.content.link import ATLink

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from sc.galleria.support.browser.galleria import Galleria
from sc.galleria.support.interfaces import IGeneralSettings
from sc.galleria.support.testing import INTEGRATION_TESTING


class BrowserViewTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.user = self.portal['portal_membership'].getAuthenticatedMember()

    def test_galleria_picasauserandid_with_link(self):
        """ Check that gets the user id and picasa id in a tuple from
            the picasa link.
        """
        link = ATLink(self.user)
        link.setRemoteUrl('https://picasaweb.google.com/user_id/galleria_id')
        galleria = Galleria(link, self.request)
        self.assertEquals(galleria.plugins(plname='picasaweb'),
                          ('user_id', 'galleria_id'))

    def test_galleria_flickrid_with_link(self):
        """ Check that gets the flickr id from the flickr link.
        """
        self.portal.invokeFactory('Link', 'flickr_link')
        link = self.portal['flickr_link']
        link.setRemoteUrl(
            'http://www.flickr.com/photos/user_id/sets/galleria_id/')
        galleria = Galleria(link, self.request)
        self.assertEquals(galleria.plugins(plname='flickr'), 'galleria_id')

    def test_portal_url(self):
        galleria = Galleria(self.user, self.request)
        self.assertEquals(galleria.portal_url(), self.portal.absolute_url())

    def test_galleriajs_no_link(self):
        """ Check that galleriajs method render javascript code with
            default values when context is not a link.
        """
        galleria = Galleria(self.user, self.request)
        js = galleria.galleriajs()
        result = {
            "Galleria.run": "('#content-galleria'",
            "width: ": '500',
            "height: ": '500',
            "autoplay: ": 'true',
            "wait: ": '5000',
            "showInfo: ": 'true',
            "imagePosition: ": "'center'",
            "transition: ": "'fade'",
            "transitionSpeed: ": '400',
            "lightbox: ": 'false',
            "showCounter: ": 'true',
            "showImagenav: ": 'true',
            "swipe: ": 'true',
            "dummy: ": "'%s'" % (self.portal.absolute_url() + \
                        '/++resource++galleria-images/dummy.png'),
            "thumbnails: ": 'true',
            "debug: ": 'false',
            }
        for key in result.keys():
            self.assertTrue(key + result[key] in js)

    def test_galleriajs_with_link_flickr(self):
        """ Check that galleriajs method render javascript code with
            default values when context is a flickr link .
        """
        link = ATLink(self.user)
        link.setRemoteUrl(
            'http://www.flickr.com/photos/user_id/sets/galleria_id/')
        galleria = Galleria(link, self.request)
        galleria.flickrplugin.flickr = True
        js = galleria.galleriajs()
        result = {
            "jQuery": "('#content-galleria')",
            "set = ": "'galleria_id'",
            "max: ": '20',
            "description: ": 'false',
            "width: ": '500',
            "height: ": '500',
            "autoplay: ": 'true',
            }
        for key in result.keys():
            self.assertTrue(key + result[key] in js)

    def test_galleriajs_with_link_picasa(self):
        """ Check that galleriajs method render javascript code with
            default values when context is a picasa link.
        """
        link = ATLink(self.user)
        link.setRemoteUrl('https://picasaweb.google.com/user_id/galleria_id')
        galleria = Galleria(link, self.request)
        galleria.picasaplugin.picasa = True
        js = galleria.galleriajs()
        result = {
            "jQuery": "('#content-galleria')",
            "max: ": '20',
            "description: ": 'false',
            "picasa.useralbum": """( 'user_id', 'galleria_id',""",
            "width: ": '500',
            "height: ": '500',
            "autoplay: ": 'true',
            }
        for key in result.keys():
            self.assertTrue(key + result[key] in js)
