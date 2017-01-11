# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from sc.galleria.support.config import PROJECTNAME

import logging


logger = logging.getLogger(PROJECTNAME)

TYPES = {
    'Collection': 'standard_view',
    'Folder': 'folder_listing',
    'Link': 'link_redirect_view',
    'Topic': 'atct_topic_view',
}


def remove_galleria_view_from_content(portal):
    """Remove galleria_view from content intances."""
    catalog = getToolByName(portal, 'portal_catalog')

    for t, default_view in TYPES.iteritems():
        results = catalog(portal_type=t)
        logger.info('{0} objects of type {1} found'.format(len(results), t))
        for brain in results:
            obj = brain.getObject()
            if obj.getLayout() != 'galleria_view':
                continue
            obj.setLayout(default_view)
            logger.info('{0} layout changed from "galleria_view" to "{1}"'.format(
                brain.getPath(), default_view))

    logger.info('"galleria_view" removed from all content')


def revert_portal_types_view_methods(portal):
    """Remove galleria_view from portal types view_methods."""
    types_tool = getToolByName(portal, 'portal_types')

    for t in TYPES.keys():
        view_methods = list(types_tool[t].view_methods)
        view_methods = tuple(x for x in view_methods if x != 'galleria_view')
        types_tool[t].view_methods = view_methods

    logger.info('"galleria_view" removed from portal types view methods')


def uninstall(portal, reinstall=False):
    if not reinstall:
        remove_galleria_view_from_content(portal)
        revert_portal_types_view_methods(portal)
        profile = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
