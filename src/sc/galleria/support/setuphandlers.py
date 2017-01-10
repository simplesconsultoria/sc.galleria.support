# -*- coding: utf-8 -*-
import logging

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.upgrade import listUpgradeSteps

_PROJECT = 'sc.galleria.support'
_PROFILE_ID = 'sc.galleria.support:default'


def install(context):
    '''
     Ordinarily, GenericSetup handlers check for the existence of XML files.
     Here, we are not parsing an XML file, but we use this text file as a
     flag to check that we actually meant for this import step to be run.
     The file is found in profiles/default.
    '''
    if context.readDataFile('sc.galleria.support_default.txt') is None:
        return


def remove_galleria_view(portal, portal_type, default_view):
    """Remove galleria_view."""
    logger = logging.getLogger(_PROJECT)
    types = getToolByName(portal, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    tp = types[portal_type]

    # remove view option
    tp.view_methods = tuple(x for x in tp.view_methods if x != 'galleria_view')
    logger.info('Remove view method "galleria_view" for content type {0}'.format(portal_type))

    # remove view to immediate_view attribute
    if tp.immediate_view == 'galleria_view':
        tp.immediate_view = default_view
        logger.info('{0} immediate_view changed from "galleria_view" to "{1}"'.format(
            portal_type, default_view))

    # remove view to default_view attribute
    if tp.default_view == 'galleria_view':
        tp.default_view = default_view
        logger.info('{0} default_view changed from "galleria_view" to "{1}"'.format(
            portal_type, default_view))

    # remove view from objects
    brains = catalog(portal_type=portal_type)
    for brain in brains:
        obj = brain.getObject()
        layout = obj.getLayout()
        if layout != 'galleria_view':
            continue
        obj.setLayout(default_view)
        logger.info('{0} layout changed from "galleria_view" to "{1}"'.format(
            brain.getPath(), default_view))


def uninstall(context):
    '''Run uninstall steps.'''

    if context.readDataFile('sc.galleria.support_uninstall.txt') is None:
        return

    logger = logging.getLogger(_PROJECT)
    portal = context.getSite()

    remove_galleria_view(portal, 'Collection', 'standard_view')
    remove_galleria_view(portal, 'Folder', 'folder_listing')
    remove_galleria_view(portal, 'Link', 'link_redirect_view')
    remove_galleria_view(portal, 'Topic', 'atct_topic_view')
    logger.info('"galleria_view" removed')

    portal_conf = getToolByName(portal, 'portal_controlpanel')
    portal_conf.unregisterConfiglet('@@galleria-settings')
    logger.info('"@@galleria-settings" controlpanel removed')


def add_galleria_js(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(_PROJECT)

    profile = 'profile-collective.js.galleria:default'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)


PREVIOUS = ('++resource++galleria.js',)


def from1001_to1002(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(_PROJECT)

    jsregistry = getToolByName(context, 'portal_javascripts')
    for PREV in PREVIOUS:
        jsregistry.unregisterResource(PREV)
