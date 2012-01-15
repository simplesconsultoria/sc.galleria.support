# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from plone.registry import Registry

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope import component
from zope.interface import Interface
#from zope.component import getUtility
from zope.component._api import getUtility

from sc.galleria.interfaces import IGalleria, IGalleriaSettings
from sc.galleria import MessageFactory as _

class GalleriaSettingsEditForm(controlpanel.RegistryEditForm):
    """ Control Panel """
    schema = IGalleriaSettings
    label = _(u"Galleria settings")
    description = _(u"""""")

    def updateFields(self):
        super(GalleriaSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(GalleriaSettingsEditForm, self).updateWidgets()

class GalleriaSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = GalleriaSettingsEditForm 


class Galleria(BrowserView):
    """ Used by browser view
    """
    implements(IGalleria)

    def __init__(self, context, request,*args,**kwargs):
        super(Galleria, self).__init__(context, request,*args,**kwargs)
        context = aq_inner(context)
        self.context = context
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IGalleriaSettings)


    def portal_url(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name="plone_portal_state")
        return portal_state.portal_url()

    def setting(self):
        return """jQuery('#content-core').galleria({
                   width: %s,
                   height: %s,
                   autoplay: %s,
                   showInfo: %s,
                   imagePosition: '%s',
                   transition: '%s',
                   transitionSpeed: %s,
                   lightbox: %s,
                   showCounter: %s,
                   showImagenav: %s,
                   swipe: %s,
                   dummy: '%s',
                   debug: %s,}) """ %(int(self.settings.image_width),
                                     int(self.settings.image_height),
                                     str(self.settings.autoplay).lower(),
                                     str(self.settings.showInf).lower(),
                                     str(self.settings.imagePosition),
                                     self.settings.transitions,
                                     int(self.settings.transitionSpeed),
                                     str(self.settings.lightbox).lower(),
                                     str(self.settings.showCounting).lower(),
                                     str(self.settings.showimagenav).lower(),
                                     str(self.settings.swipe).lower(),
                                     str(self.portal_url() + '/++resource++dummy_galleria.png'),
                                     str(self.settings.debug).lower())

