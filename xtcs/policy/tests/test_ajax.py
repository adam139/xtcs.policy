# -*- coding: UTF-8 -*-
from hashlib import sha1 as sha
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.keyring.interfaces import IKeyManager
from plone.namedfile.file import NamedImage
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from Products.Five.utilities.marker import mark
from xtcs.policy.interfaces import IJuanzenggongshi as ifobj
from xtcs.policy.testing import FunctionalTesting
from zope.component import getUtility
from zope.interface import alsoProvides

import hmac
import json
import os
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
        portal.invokeFactory('Folder', 'cishanzixun')
        portal['cishanzixun'].invokeFactory('Folder', 'gongyixinwen',
                                            title=u"公益新闻",
                                            description=u"公益新闻")
        portal.invokeFactory('Folder', 'aixingongshi')

        portal['aixingongshi'].invokeFactory('Folder', 'juanzenggongshi',
                                             title=u"捐赠公示",
                                             description=u"捐赠公示")

        self.target = portal['aixingongshi']['juanzenggongshi']
        mark(self.target, ifobj)
        self.portal = portal

    def test_donate_search(self):
        request = self.layer['request']
#         from emc.theme.interfaces import IThemeSpecific
#         alsoProvides(request, IThemeSpecific)
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
            '_authenticator': auth,
            'start': 0,
            'size': 10,
            'id': 0,
            'multi': 1,
        }
# Look up and invoke the view via traversal
        target = self.target
        view = target.restrictedTraverse('@@donate_ajaxsearch')
        result = view()
        outstr = u'\u201c4\xb714\u201d\u9752\u6d77\u7389\u6811\u5730\u9707\u6350\u6b3e\u516c\u793a'
        self.assertTrue(outstr in json.loads(result)['searchresult'])
        self.assertEqual(json.loads(result)['total'], 4)

    def test_donor_search(self):
        request = self.layer['request']
#         from emc.theme.interfaces import IThemeSpecific
#         alsoProvides(request, IThemeSpecific)
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
            '_authenticator': auth,
            'start': 0,
            'size': 10,
            'id': 18,
            'multi': 1,
        }
# Look up and invoke the view via traversal
        target = self.target
        view = target.restrictedTraverse('@@donor_ajaxsearch')
        result = view()
        outstr = u'\u201c4\xb714\u201d\u9752\u6d77\u7389\u6811\u5730\u9707\u6350\u6b3e\u516c\u793a'
#         self.assertTrue(outstr in json.loads(result)['searchresult'])
        self.assertEqual(json.loads(result)['total'], 156)
