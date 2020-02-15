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



def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        for item in STRUCTURE:
            _create_content(item, portal)         
    
    def test_sort_on(self):
# check collection sort_on,sort_reversed etc.        

        portal = self.layer['portal']
        item = portal['sqls']['gongyixinwen']  
        self.assertTrue(item.sort_on == "created")
        self.assertTrue(item.sort_reversed == True)      

  