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
        obj = portal.absolute_url() + '/@@auth'    
        browser.open(obj) 
        outstr = "pay"
        self.assertTrue(outstr in browser.contents)
        obj = portal.absolute_url() + '/@@hotauth'    
        browser.open(obj) 
        outstr = "hotpay"
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
        obj = portal.absolute_url() + '/@@donated_workflow'    
        browser.open(obj)
 
        outstr = 'http://nohost/plone/@@hotauth'
        self.assertTrue(outstr in browser.contents)
        
    def test_zhifu_weixin_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       

        import transaction
        transaction.commit()        
        obj = portal.absolute_url() + '/@@pay?code=2&mail=3'    
        browser.open(obj)
 
        outstr = 'name="money"'

        self.assertTrue(outstr in browser.contents)        

    def test_hot_zhifu_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       

        import transaction
        transaction.commit()        
        obj = portal.absolute_url() + '/@@hotpay?code=2&mail=3'    
        browser.open(obj)
 
        outstr = 'name="money"'

        self.assertTrue(outstr in browser.contents)
        
    def test_ajax_search(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
#                         '_authenticator': auth,
                        'fee': 10,
                        'code':12,
                        'aname':'testuser',
                        'did':'11',
                        'openid':'oQ61n01gs3t34TglBy_x2U6l8VWk',                                                                                                                    
                        }
# Look up and invoke the view via traversal
        view = self.portal.restrictedTraverse('@@pay_ajax')
        result = view()
        self.assertEqual(len(json.loads(result)),6)         
  