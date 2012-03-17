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

    def __init__(self, context, request,*args,**kwargs):
        super(Galleria, self).__init__(context, request,*args,**kwargs)
        context = aq_inner(context)
        self.context = context
        self.ptype = self.context.portal_type
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IGeneralSettings)
        self.flickrplugin = self.registry.forInterface(IFlickrPlugin)
        self.picasaplugin = self.registry.forInterface(IPicasaPlugin)
        self.historyplugin = self.registry.forInterface(IHistoryPlugin)

    def galleria_picasauserandid(self):
        if self.ptype == 'Link':
            id_list = self.context.remote_url().split('/')
            try:
               if len(id_list) == 5 and id_list[2].find('picasaweb') >=0:
                   galluserid,galleriaid = id_list[-2], id_list[-1]
               elif len(id_list) == 6 and id_list[2].find('picasaweb') >=0:
                   galluserid,galleriaid = id_list[-3], id_list[-2]
               else:
                    galluserid,galleriaid = (None,None)
            except:
                    galluserid,galleriaid = (None,None)

            return (galluserid,galleriaid)

    def galleria_flickrid(self):
        if self.ptype == 'Link':
            positionsets = int(str(self.context.remote_url()).find('sets'))
            id_list = self.context.remote_url()[positionsets:].split('/')
            try:
               if len(id_list) == 3 and id_list[2].find('flickr'):
                   galleriaid = id_list[-2]
               elif len(id_list) == 2 and id_list[2].find('flickr'):
                   galleriaid = id_list[-1]
               else:
                    galleriaid = None
            except:
                galleriaid = None

            return galleriaid

    def portal_url(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name="plone_portal_state")
        return portal_state.portal_url()

    def getThumbnails(self):
        if self.settings.thumbnails == 'show':
            return str(True).lower()
        else:
            return "'%s'" %(self.settings.thumbnails)

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
                             debug: %s,}) }) """ %(str(self.settings.selector),
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
                                              self.getThumbnails(),
                                              str(self.settings.debug).lower())

        elif self.ptype == 'Link' and self.flickrplugin.flickr and self.galleria_flickrid():
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
                      }) """ %(str(self.settings.selector),
                               str(self.galleria_flickrid()),
                               int(self.flickrplugin.flickr_max),
                               str(self.flickrplugin.flickr_desc).lower(),
                               int(self.settings.gallery_width),
                               int(self.settings.gallery_height),
                               str(self.settings.autoplay).lower())
        elif self.ptype == 'Link' and self.picasaplugin.picasa and self.galleria_picasauserandid()[0]:
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
                      }) """ %(str(self.settings.selector),
                               int(self.picasaplugin.picasa_max),
                               str(self.picasaplugin.picasa_desc).lower(),
                               str(self.galleria_picasauserandid()[0]),
                               str(self.galleria_picasauserandid()[1]),
                               int(self.settings.gallery_width),
                               int(self.settings.gallery_height),
                               str(self.settings.autoplay).lower())
