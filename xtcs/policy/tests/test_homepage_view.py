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
from plone.namedfile.file import NamedBlobImage,NamedBlobFile,NamedImage
import os
from plone.app.textfield.value import RichTextValue
from xtcs.policy.mapping_db import  Article

from zope.component import getUtility
from xtcs.policy import Session as session

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import datetime
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        for item in STRUCTURE:
            _create_content(item, portal)        
          
             
        data = getFile('image.jpg').read()
        item = portal['cishanzixun']['tupianxinwen']['prdt1']
        item.image = NamedBlobImage(data, 'image/jpg', u'image.jpg')
        item.text = u"图片新闻1"
        item = portal['cishanzixun']['tupianxinwen']['prdt2']
        item.image = NamedBlobImage(data, 'image/jpg', u'image.jpg')
        item.text = u"图片新闻2"
        item = portal['cishanzixun']['tupianxinwen']['prdt3']
        item.image = NamedBlobImage(data, 'image/jpg', u'image.jpg')
        item.text = u"图片新闻3"                                                                                                                          
        self.portal = portal
    
    def test_homepage_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       

        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@index.html'    
        browser.open(obj)
 
        outstr = u"图片新闻3"
        self.assertTrue(outstr in browser.contents)
        
    def test_folder_ajax_view(self):        
        request = self.layer['request']       
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'formstart': 2,
                        'size':10, 
                        'id':0,
                        'multi':1,                                                                      
                        }
# Look up and invoke the view via traversal
        target = self.portal['cishanzixun']['cishandongtai']
        view = target.restrictedTraverse('@@favoritemore')
        result = view()
        outstr = u'class="col-md-9 title"'
        self.assertTrue(outstr in json.loads(result)['outhtml'])
      
        
    def test_folder_view(self):        

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       

        import transaction
        transaction.commit()
        target = self.portal['cishanzixun']['cishandongtai']
        page = target.absolute_url() + '/@@tableview'    
        browser.open(page)
 
        outstr = 'id="tablecontent"'
        self.assertTrue(outstr in browser.contents)      

  