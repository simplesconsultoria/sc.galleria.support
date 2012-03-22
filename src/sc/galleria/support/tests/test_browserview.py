# -*- coding: utf-8 -*-

import unittest2 as unittest

from sc.galleria.support.testing import INTEGRATION_TESTING


class BrowserViewTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.user = self.portal['portal_membership'].getAuthenticatedMember()

    def test_galleria_picasauserandid_no_link(self):
        from sc.galleria.support.browser.galleria import Galleria
        galleria = Galleria(self.user, self.request)
        self.assertEquals(galleria.galleria_picasauserandid(), None)

    def test_galleria_flickrid_no_link(self):
        from sc.galleria.support.browser.galleria import Galleria
        galleria = Galleria(self.user, self.request)
        self.assertEquals(galleria.galleria_flickrid(), None)

    def test_galleria_picasauserandid_with_link(self):
        from Products.ATContentTypes.content.link import ATLink
        from sc.galleria.support.browser.galleria import Galleria
        link = ATLink(self.user)
        link.setRemoteUrl('https://picasaweb.google.com/user_id/galleria_id')
        galleria = Galleria(link, self.request)
        self.assertEquals(galleria.galleria_picasauserandid(),
                          ('user_id', 'galleria_id'))

    def test_galleria_flickrid_with_link(self):
        from Products.ATContentTypes.content.link import ATLink
        from sc.galleria.support.browser.galleria import Galleria
        link = ATLink(self.user)
        link.setRemoteUrl(
            'http://www.flickr.com/photos/user_id/sets/galleria_id/')
        galleria = Galleria(link, self.request)
        self.assertEquals(galleria.galleria_flickrid(), 'galleria_id')

    def test_portal_url(self):
        from sc.galleria.support.browser.galleria import Galleria
        galleria = Galleria(self.user, self.request)
        self.assertEquals(galleria.portal_url(), self.portal.absolute_url())

    def test_getThumbnails(self):
        from sc.galleria.support.browser.galleria import Galleria
        galleria = Galleria(self.user, self.request)
        self.assertEquals(galleria.getThumbnails(), 'true')

    def js_values_no_link(self, view):
        from sc.galleria.support.interfaces import IGeneralSettings
        result = {
            "jQuery": "('%s')" %
                    str(IGeneralSettings.get('selector').default),
            "width: ": str(IGeneralSettings.get('gallery_width').default),
            "height: ": str(IGeneralSettings.get('gallery_height').default),
            "autoplay: ":
                    str(IGeneralSettings.get('autoplay').default).lower(),
            "wait: ": str(IGeneralSettings.get('gallery_wait').default),
            "showInfo: ": str(IGeneralSettings.get('showInf').default).lower(),
            "imagePosition: ": "'%s'" %
                    str(IGeneralSettings.get('imagePosition').default),
            "transition: ": "'%s'" %
                    IGeneralSettings.get('transitions').default,
            "transitionSpeed: ":
                    str(IGeneralSettings.get('transitionSpeed').default),
            "lightbox: ":
                    str(IGeneralSettings.get('lightbox').default).lower(),
            "showCounter: ":
                    str(IGeneralSettings.get('showCounting').default).lower(),
            "showImagenav: ":
                    str(IGeneralSettings.get('showimagenav').default).lower(),
            "swipe: ": str(IGeneralSettings.get('swipe').default).lower(),
            "dummy: ": "'%s'" % (view.portal_url() + \
                        '/++resource++galleria-images/dummy.png'),
            "thumbnails: ": view.getThumbnails(),
            "debug: ": str(IGeneralSettings.get('debug').default).lower(),
            }
        return result

    def test_galleriajs_no_link(self):
        from sc.galleria.support.browser.galleria import Galleria
        galleria = Galleria(self.user, self.request)
        js = galleria.galleriajs()
        values = self.js_values_no_link(galleria)
        for key in values.keys():
            self.assertTrue(key + values[key] in js)

    def js_values_with_link_flickr(self, view):
        from sc.galleria.support.interfaces import IGeneralSettings
        result = {
            "jQuery": "('%s')" %
                    str(IGeneralSettings.get('selector').default),
            "set = ": "'%s'" % str(view.galleria_flickrid()),
            "max: ": str(view.flickrplugin.flickr_max),
            "description: ": str(view.flickrplugin.flickr_desc).lower(),
            "width: ": str(IGeneralSettings.get('gallery_width').default),
            "height: ": str(IGeneralSettings.get('gallery_height').default),
            "autoplay: ":
                    str(IGeneralSettings.get('autoplay').default).lower(),
            }
        return result

    def test_galleriajs_with_link_flickr(self):
        from Products.ATContentTypes.content.link import ATLink
        from sc.galleria.support.browser.galleria import Galleria
        link = ATLink(self.user)
        link.setRemoteUrl(
            'http://www.flickr.com/photos/user_id/sets/galleria_id/')
        galleria = Galleria(link, self.request)
        galleria.flickrplugin.flickr = True
        js = galleria.galleriajs()
        values = self.js_values_with_link_flickr(galleria)
        for key in values.keys():
            self.assertTrue(key + values[key] in js)

    def js_values_with_link_picasa(self, view):
        from sc.galleria.support.interfaces import IGeneralSettings
        result = {
            "jQuery": "('%s')" %
                    str(IGeneralSettings.get('selector').default),
            "max: ": str(view.flickrplugin.flickr_max),
            "description: ": str(view.flickrplugin.flickr_desc).lower(),
            "picasa.useralbum": """( '%s', '%s',""" % \
                            (str(view.galleria_picasauserandid()[0]),
                                str(view.galleria_picasauserandid()[1])),
            "width: ": str(IGeneralSettings.get('gallery_width').default),
            "height: ": str(IGeneralSettings.get('gallery_height').default),
            "autoplay: ":
                    str(IGeneralSettings.get('autoplay').default).lower(),
            }
        return result

    def test_galleriajs_with_link_picasa(self):
        from Products.ATContentTypes.content.link import ATLink
        from sc.galleria.support.browser.galleria import Galleria
        link = ATLink(self.user)
        link.setRemoteUrl('https://picasaweb.google.com/user_id/galleria_id')
        galleria = Galleria(link, self.request)
        galleria.picasaplugin.picasa = True
        js = galleria.galleriajs()
        values = self.js_values_with_link_picasa(galleria)
        for key in values.keys():
            self.assertTrue(key + values[key] in js)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
