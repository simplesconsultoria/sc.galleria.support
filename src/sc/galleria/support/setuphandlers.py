# -*- coding: utf-8 -*-
import logging

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.upgrade import listUpgradeSteps

_PROJECT = 'sc.galleria.support'
_PROFILE_ID = 'sc.galleria.support:default'


def install(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('sc.galleria.support_default.txt') is None:
        return


def run_upgrades(context):
    ''' Run Upgrade steps
    '''
    if context.readDataFile('sc.galleria.support_default.txt') is None:
        return
    logger = logging.getLogger(_PROJECT)
    setup_tool = getToolByName(context, 'portal_setup')
    version = setup_tool.getLastVersionForProfile(_PROFILE_ID)
    upgradeSteps = listUpgradeSteps(setup_tool, _PROFILE_ID, version)
    sorted(upgradeSteps, key=lambda step: step['sortkey'])

    for step in upgradeSteps:
        oStep = step.get('step')
        if oStep is not None:
            oStep.doStep(setup_tool)
            msg = "Ran upgrade step %s for profile %s" % (oStep.title,
                                                          _PROFILE_ID)
            setup_tool.setLastVersionForProfile(_PROFILE_ID, oStep.dest)
            logger.info(msg)


def uninstall(context):
    ''' Run uninstall steps
    '''

    if context.readDataFile('sc.galleria.support_uninstall.txt') is None:
        return

    portal_conf = getToolByName(context, 'portal_controlpanel')
    portal_conf.unregisterConfiglet('@@galleria-settings')


def add_galleria_js(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(_PROJECT)

    profile = 'profile-collective.js.galleria:default'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)
