# -*- coding: UTF-8 -*-
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from Products.Five.utilities.marker import mark
from xtcs.policy.interfaces import IJuanzenggongshi as specifyifobj
from xtcs.policy.interfaces import IYangguangwu as ifobj
from xtcs.policy.testing import FunctionalTesting
from zope.dottedname.resolve import resolve

import unittest


class TestView(unittest.TestCase):

    layer = FunctionalTesting

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        portal.invokeFactory('Folder', 'aixingongshi')

        portal['aixingongshi'].invokeFactory('Folder', 'juanzenggongshi',
                                             title=u"捐赠公示",
                                             description=u"捐赠公示")

        self.specifytarget = portal['aixingongshi']['juanzenggongshi']
        mark(self.specifytarget, specifyifobj)
        portal['aixingongshi'].invokeFactory('Folder', 'yangguangwu',
                                             title=u"阳光屋",
                                             description=u"阳光屋")

        self.target = portal['aixingongshi']['yangguangwu']
        mark(self.target, ifobj)
        self.portal = portal

    def test_aixingongshi_view(self):

        app = self.layer['app']
        portal = self.portal
        target = self.target

        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization', 'Basic %s:%s' %
            (TEST_USER_NAME, TEST_USER_PASSWORD,))

        import transaction
        transaction.commit()
        obj = target.absolute_url() + '/@@donate_listings'

        browser.open(obj)

        outstr = 'id="ajaxsearch"'

        self.assertTrue(outstr in browser.contents)

    def test_juanxian_view(self):
        """捐赠记录
        """

        app = self.layer['app']
        portal = self.portal
        target = self.target

        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization', 'Basic %s:%s' %
            (TEST_USER_NAME, TEST_USER_PASSWORD,))

        import transaction
        transaction.commit()
        obj = target.absolute_url() + '/@@donor_listings'

        browser.open(obj)

        outstr = 'id="ajaxsearch"'

        self.assertTrue(outstr in browser.contents)

    def test_juanxian_view(self):
        """日常捐赠记录
        """

        app = self.layer['app']
        portal = self.portal
        target = self.specifytarget

        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization', 'Basic %s:%s' %
            (TEST_USER_NAME, TEST_USER_PASSWORD,))

        import transaction
        transaction.commit()
        obj = target.absolute_url() + '/@@specify_donor_listings'

        browser.open(obj)

        outstr = 'id="ajaxsearch"'

        self.assertTrue(outstr in browser.contents)
