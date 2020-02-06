#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from plone.keyring.interfaces import IKeyManager
from Products.CMFCore.utils import getToolByName
from xtcs.policy.setuphandlers import STRUCTURE,_create_content 
from xtcs.policy.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from zope.component import getUtility


class TestView(unittest.TestCase):
    
    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))                                                                                                                        
        self.portal = portal
    
    def test_zhifu_weixin_auth_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       

        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@auth.html'    
        browser.open(obj)
 
        outstr = "wx2833460b1571bd01"
        import pdb
        pdb.set_trace()
        self.assertTrue(outstr in browser.contents)
        
    def test_zhifu_weixin_workflow_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       


        from zope.interface import alsoProvides
        from xtcs.policy.interfaces import IJuanzengworkflow
        alsoProvides(portal,IJuanzengworkflow)
        import transaction
        transaction.commit()        
        obj = portal.absolute_url() + '/@@donated_workflow?code=2&mail=3'    
        browser.open(obj)
 
        outstr = "wx2833460b1571bd01"
        self.assertTrue(outstr in browser.contents)
        
        
    def test_ajax_search(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'fee': 10,
                        'did':'21' ,
                        'openid':'oQ61n01gs3t34TglBy_x2U6l8VWk',                                                                                                                    
                        }
# Look up and invoke the view via traversal
        view = self.portal.restrictedTraverse('@@pay_ajax')
        result = view()


        self.assertEqual(json.loads(result),10)         
  