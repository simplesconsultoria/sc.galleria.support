# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from plone.registry import Registry

from plone.z3cform import layout

from z3c.form import field

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope import component
from zope.interface import Interface
from zope.component._api import getUtility
from zope.interface import alsoProvides

from sc.galleria.support.interfaces import IGalleria,\
                                            IGalleriaSettings,\
                                            IGeneralSettings,\
                                            FormGroup1,\
                                            FormGroup2,\
                                            FormGroup3,\
                                            IFlickrPlugin,\
                                            IPicasaPlugin,\
                                            IHistoryPlugin

from sc.galleria.support import MessageFactory as _

from urlparse import urlparse, urlunparse
from cgi import parse_qs
from urllib import urlencode
import types


class GalleriaSettingsEditForm(controlpanel.RegistryEditForm):
    """ Control Panel """
    schema = IGalleriaSettings
    fields = field.Fields(IGeneralSettings)
    groups = FormGroup1, FormGroup2, FormGroup3
    label = _(u"Galleria settings")
    description = _(u"""""")

    def updateFields(self):
        super(GalleriaSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(GalleriaSettingsEditForm, self).updateWidgets()

    def getContent(self):
        return AbstractRecordsProxy(self.schema)


class GalleriaSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = GalleriaSettingsEditForm


class AbstractRecordsProxy(object):
    """Multiple registry schema proxy.

    This class supports schemas that contain derived fields. The
    settings will be stored with respect to the individual field
    interfaces.
    """

    def __init__(self, schema):
        state = self.__dict__
        state["__registry__"] = getUtility(IRegistry)
        state["__proxies__"] = {}
        state["__schema__"] = schema
        alsoProvides(self, schema)

    def __getattr__(self, name):
        try:
            field = self.__schema__[name]
        except KeyError:
            raise AttributeError(name)
        else:
            proxy = self._get_proxy(field.interface)
            return getattr(proxy, name)

    def __setattr__(self, name, value):
        try:
            field = self.__schema__[name]
        except KeyError:
            self.__dict__[name] = value
        else:
            proxy = self._get_proxy(field.interface)
            return setattr(proxy, name, value)

    def __repr__(self):
        return "<AbstractRecordsProxy for %s>" % self.__schema__.__identifier__

    def _get_proxy(self, interface):
        proxies = self.__proxies__
        return proxies.get(interface) or \
               proxies.setdefault(interface, self.__registry__.\
                                  forInterface(interface))


class Galleria(BrowserView):
    """ Used by browser view
    """
    implements(IGalleria)

    def __init__(self, context, request, *args, **kwargs):
        super(Galleria, self).__init__(context, request, *args, **kwargs)
        context = aq_inner(context)
        self.context = context
        self.ptype = self.context.portal_type
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IGeneralSettings)
        self.flickrplugin = self.registry.forInterface(IFlickrPlugin)
        self.picasaplugin = self.registry.forInterface(IPicasaPlugin)
        self.historyplugin = self.registry.forInterface(IHistoryPlugin)
        self.isVideo = self.plugins(plname='youtube') or self.plugins(plname='vimeo') or self.plugins(plname='dailymotion')

    def plugins(self, plname=''):

        if self.ptype == 'Link':
            urllink = urlparse(self.context.remote_url())

            if type(urllink) is types.TupleType:
                params = parse_qs(urllink[4])
            else:
                params = parse_qs(urllink[4])

            urllink = {'scheme': urllink[0],
                         'netloc': urllink[1],
                         'path': urllink[2],
                         'params': urllink[3],
                         'query': urllink[4],
                         'fragment': urllink[5]}

            if plname == 'youtube':
                if urllink['netloc'].find(plname) >= 0:
                    new_params = {'v': params['v'][0]}
                    cleaned_url = urlunparse((urllink['scheme'], urllink['netloc'], urllink['path'], None, urlencode(new_params), urllink['fragment']))
                    return cleaned_url
            elif plname == 'picasaweb':
                if urllink['netloc'].find(plname) >= 0:
                    id_list = urllink['path'].split('/')
                    try:
                        if len(id_list) == 3:
                            galluserid, galleriaid = urllink['path'].split('/')[1], urllink['path'].split('/')[-1]
                        elif len(id_list) == 4:
                            galluserid, galleriaid = urllink['path'].split('/')[1], urllink['path'].split('/')[-2] 
                        else:
                            galluserid, galleriaid = (None, None)
                    except:
                            galluserid, galleriaid = (None, None)
                    return (galluserid, galleriaid)
            elif plname == 'flickr':
                positionsets = int(urllink['path'].find('sets'))
                id_list = urllink['path'][positionsets:].split('/')
                try:
                    if len(id_list) == 3:
                        galleriaid = id_list[-2]
                    elif len(id_list) == 2:
                        galleriaid = id_list[-1]
                    else:
                        galleriaid = None
                except:
                    galleriaid = None
                return galleriaid
            elif plname == 'vimeo' or plname == 'dailymotion':
                if urllink['netloc'].find(plname) >= 0:
                    cleaned_url = urlunparse((urllink['scheme'], urllink['netloc'], urllink['path'], None, urlencode(params), urllink['fragment']))
                    return cleaned_url
                else:
                    pass

    def portal_url(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name="plone_portal_state")
        return portal_state.portal_url()

    def getThumbnails(self, videoval=[]):
        if type(videoval) is types.IntType:
            if videoval == 1:
                if self.settings.thumbnails == 'show':
                    return str(True).lower()
                else:
                    return "'%s'" % (self.settings.thumbnails)
            else:
                return 'false'
        elif type(videoval) is types.ListType:
            if len(videoval) == 0 or len(videoval) == 1:
                return 'false'
            else:
                if self.settings.thumbnails == 'show':
                    return str(True).lower()
                else:
                    return "'%s'" % (self.settings.thumbnails)

    def galleriajs(self):
        """ Load default gallery """
        if self.ptype != 'Link':
            return """jQuery(document).ready(function(){
                         jQuery('%s').galleria({
                             width: %s,
                             height: %s,
                             autoplay: %s,
                             wait: %s,
                             showInfo: %s,
                             imagePosition: '%s',
                             transition: '%s',
                             transitionSpeed: %s,
                             lightbox: %s,
                             showCounter: %s,
                             showImagenav: %s,
                             swipe: %s,
                             dummy: '%s',
                             thumbnails: %s,
                             thumbQuality: 'false',
                             debug: %s,}) }) """ % (str(self.settings.selector),
                                              int(self.settings.gallery_width),
                                              int(self.settings.gallery_height),
                                              str(self.settings.autoplay).lower(),
                                              int(self.settings.gallery_wait),
                                              str(self.settings.showInf).lower(),
                                              str(self.settings.imagePosition),
                                              self.settings.transitions,
                                              int(self.settings.transitionSpeed),
                                              str(self.settings.lightbox).lower(),
                                              str(self.settings.showCounting).lower(),
                                              str(self.settings.showimagenav).lower(),
                                              str(self.settings.swipe).lower(),
                                              str(self.portal_url() + '/++resource++galleria-images/dummy.png'),
                                              self.getThumbnails(videoval=1),
                                              str(self.settings.debug).lower())

        if self.ptype == 'Link' and self.flickrplugin.flickr and self.plugins(plname='flickr'):
            """ Load Flickr plugin """
            return """jQuery(document).ready(function(){
                          var flickr = new Galleria.Flickr();
                          var elem = jQuery('%s');
                          var set = '%s';

                          flickr.setOptions({
                              max: %s,
                              description: %s,
                          })

                          flickr.set(set, function(data) {
                             if(jQuery('.galleria-container notouch').length){
                                 Galleria.get(0).load(data);
                             } else{
                                 elem.galleria({
                                     width: %s,
                                     height: %s,
                                     autoplay: %s,
                                     dataSource: data,
                                 });

                                 Galleria.get(0).load(data);
                             }

                          })
                      }) """ % (str(self.settings.selector),
                               str(self.plugins(plname='flickr')),
                               int(self.flickrplugin.flickr_max),
                               str(self.flickrplugin.flickr_desc).lower(),
                               int(self.settings.gallery_width),
                               int(self.settings.gallery_height),
                               str(self.settings.autoplay).lower())
        elif self.ptype == 'Link' and self.picasaplugin.picasa and self.plugins(plname='picasaweb'):
            """ Load Picasa plugin """
            return """jQuery(document).ready(function(){
                          var picasa = new Galleria.Picasa();
                          var elem = jQuery('%s');

                          picasa.setOptions({
                              max: %s,
                              description: %s,
                          })

                          picasa.useralbum( '%s', '%s',function(data) {
                             if(jQuery('.galleria-container notouch').length){
                                 Galleria.get(0).load(data);
                             } else{
                                 elem.galleria({
                                     width: %s,
                                     height: %s,
                                     autoplay: %s,
                                     dataSource: data,
                                 });

                                 Galleria.get(0).load(data);
                             }

                          })
                      }) """ % (str(self.settings.selector),
                               int(self.picasaplugin.picasa_max),
                               str(self.picasaplugin.picasa_desc).lower(),
                               str(self.plugins(plname='picasaweb')[0]),
                               str(self.plugins(plname='picasaweb')[1]),
                               int(self.settings.gallery_width),
                               int(self.settings.gallery_height),
                               str(self.settings.autoplay).lower())
        elif self.plugins(plname='youtube') or self.plugins(plname='vimeo') or self.plugins(plname='dailymotion'):
            video_url = self.plugins(plname='youtube') or self.plugins(plname='vimeo') or self.plugins(plname='dailymotion')
            return """jQuery(document).ready(function(){
                         jQuery('%s').galleria({
                             width: %s,
                             height: %s,
                             autoplay: %s,
                             wait: %s,
                             showInfo: %s,
                             imagePosition: '%s',
                             transition: '%s',
                             transitionSpeed: %s,
                             showCounter: %s,
                             showImagenav: %s,
                             swipe: %s,
                             dummy: '%s',
                             thumbnails: %s,
                             thumbQuality: 'false',
                             dataSource: [{ 'video': '%s' },],
                             debug: %s,}) }) """ % (str(self.settings.selector),
                                              int(self.settings.gallery_width),
                                              int(self.settings.gallery_height),
                                              str(self.settings.autoplay).lower(),
                                              int(self.settings.gallery_wait),
                                              str(self.settings.showInf).lower(),
                                              str(self.settings.imagePosition),
                                              self.settings.transitions,
                                              int(self.settings.transitionSpeed),
                                              str(self.settings.showCounting).lower(),
                                              str(self.settings.showimagenav).lower(),
                                              str(self.settings.swipe).lower(),
                                              str(self.portal_url() + '/++resource++galleria-images/dummy.png'),
                                              self.getThumbnails(),
                                              video_url,
                                              str(self.settings.debug).lower())
