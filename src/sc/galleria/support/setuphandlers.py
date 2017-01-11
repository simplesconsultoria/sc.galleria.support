# -*- coding: utf-8 -*-
import logging

from Products.CMFCore.utils import getToolByName

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
