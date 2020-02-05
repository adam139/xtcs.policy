#-*- coding: UTF-8 -*-
import datetime
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting,FunctionalTesting

from plone.app.testing import (
IntegrationTesting,
FunctionalTesting,
login, logout, setRoles,
PLONE_FIXTURE,
TEST_USER_NAME,
SITE_OWNER_NAME,
)

from plone.testing import z2
from plone.namedfile.file import NamedImage
from plone import namedfile
from zope.configuration import xmlconfig

def getFile(filename):
    """ return contents of the file with the given name """
    import os
    filename = os.path.join(os.path.dirname(__file__) + "/tests/", filename)
    return open(filename, 'r')

class SitePolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import xtcs.policy
        import plone.app.contenttypes
        import xtcs.theme
        import my315ok.products
        import my315ok.wechat
        xmlconfig.file('configure.zcml', plone.app.contenttypes, context=configurationContext)
        xmlconfig.file('configure.zcml', my315ok.products, context=configurationContext)
        xmlconfig.file('configure.zcml', my315ok.wechat, context=configurationContext)
        xmlconfig.file('configure.zcml', xtcs.theme, context=configurationContext)
        xmlconfig.file('configure.zcml', xtcs.policy, context=configurationContext)        
       
    
    def tearDownZope(self, app):
        pass
        # Uninstall products installed above
        
        
    def setUpPloneSite(self, portal):

        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'my315ok.wechat:default')
        applyProfile(portal, 'my315ok.products:default') 
        applyProfile(portal, 'xtcs.policy:default')       


class IntegrationSitePolicy(SitePolicy):      
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'my315ok.products:default') 
        applyProfile(portal, 'xtcs.policy:default')
        applyProfile(portal, 'plone.app.contenttypes:default')

        #make global request work
        from zope.globalrequest import setRequest
        setRequest(portal.REQUEST)
        # login doesn't work so we need to call z2.login directly
        z2.login(portal.__parent__.acl_users, SITE_OWNER_NAME)
#        setRoles(portal, TEST_USER_ID, ('Manager',))
#        login(portal, TEST_USER_NAME)
              
        self.portal = portal 

POLICY_FIXTURE = SitePolicy()
POLICY_INTEGRATION_FIXTURE = IntegrationSitePolicy()
POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(POLICY_INTEGRATION_FIXTURE,), name="Site:Integration")
FunctionalTesting = FunctionalTesting(bases=(POLICY_FIXTURE,), name="Site:FunctionalTesting")