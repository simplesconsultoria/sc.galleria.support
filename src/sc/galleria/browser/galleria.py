# -*- coding: utf-8 -*-

from zope.interface import Interface
from plone.app.registry.browser import controlpanel

from sc.galleria.interfaces import IGalleriaSettings
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

