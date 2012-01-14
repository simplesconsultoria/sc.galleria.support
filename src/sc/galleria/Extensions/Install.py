# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName


def uninstall(portal, reinstall=False):

    if not reinstall:
        # normal uninstall
        setup_tool = getToolByName(portal, 'portal_setup')
        profile = 'profile-sc.galleria:uninstall'
        setup_tool.runAllImportStepsFromProfile(profile)

        return "Ran all uninstall steps."
