import unittest
import transaction
from datetime import datetime
from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from xtcs.policy.testing import FunctionalTesting,POLICY_INTEGRATION_TESTING
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from xtcs.policy.browser.interfaces import IwechatSettings
from my315ok.wechat.config import ControlPanelConf_pub 

class TestSetup(unittest.TestCase):
    
    layer = POLICY_INTEGRATION_TESTING
    

    
    def test_setting_configured(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
#         self.assertEqual(settings.appid, "wx77d2frty25808f911")
#         self.assertEqual(settings.preview, "http://www.xtcs.org/")
        st = ControlPanelConf_pub()
        import pdb
        pdb.set_trace()        
        self.assertEqual(st.CURL_TIMEOUT, 40)      

        self.assertEqual(settings.access_token_time, datetime.strptime("2014-08-14 00:00:00", '%Y-%m-%d %H:%M:%S'))



class TestControlPanel(unittest.TestCase):

    layer = FunctionalTesting


    def test_render_plone_page(self):
        
        app = self.layer['app']
        portal = self.layer['portal']        
        transaction.commit()        
        browser = Browser(app)   
        browser.open(portal.absolute_url() + "/@@wechat-controlpanel")
        self.assertTrue('<aside id="global_statusmessage">' in browser.contents)
