# -*- coding: utf-8 -*-

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import alsoProvides
from xtcs.policy.testing import POLICY_INTEGRATION_TESTING as INTEGRATION_TESTING
from xtcs.policy.testing import FunctionalTesting
import transaction
import unittest as unittest
from my315ok.wechat.lib import WeixinHelper
from xtcs.policy.browser.dbpage import CustomWeixinHelper
from my315ok.wechat.pay import WxPayConf_pub

class TestHelper(WeixinHelper):
    
    @classmethod
    def getAccessTokenByCode(cls, code):
        """通过code换取网页授权access_token, 该access_token与getAccessToken()返回是不一样的
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """
        _CODEACCESS_URL = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
        return _CODEACCESS_URL.format(WxPayConf_pub.APPID, WxPayConf_pub.APPSECRET, code)

    @classmethod
    def refreshAccessToken(cls, refresh_token):
        """刷新access_token, 使用getAccessTokenByCode()返回的refresh_token刷新access_token，可获得较长时间有效期
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """
        _REFRESHTOKRN_URL = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={0}&grant_type=refresh_token&refresh_token={1}"
        return _REFRESHTOKRN_URL.format(WxPayConf_pub.APPID, refresh_token)    


class InharitHelper(TestHelper):
    
    @classmethod
    def getAccessTokenByCode(cls, code):
        """通过code换取网页授权access_token, 该access_token与getAccessToken()返回是不一样的
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """

        code = super(InharitHelper,cls).getAccessTokenByCode(code)
        return code


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    def test_super(self):
        code = InharitHelper.getAccessTokenByCode("123")
        compute_code = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"       
        self.assertEqual(code, compute_code.format(WxPayConf_pub.APPID, WxPayConf_pub.APPSECRET, "123"))

 