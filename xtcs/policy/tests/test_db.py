#-*- coding: UTF-8 -*-
import datetime
import unittest
from zope.interface import alsoProvides
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.interfaces import IPloneFormLayer
from xtcs.policy.testing import POLICY_INTEGRATION_TESTING as INTEGRATION_TESTING
from xtcs.policy.setuphandlers import STRUCTURE,_create_content
from xtcs.policy.migration import _create_article
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark


class TestParametersDatabase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
#         self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        for item in STRUCTURE:
            _create_content(item, self.portal)

    def test_Juanzeng_table(self):

        from xtcs.policy.interfaces import IDbapi
        from zope.component import queryUtility
        from datetime import datetime,timedelta

        locator = queryUtility(IDbapi, name='juanzeng')
        # add
        args = {"status":0,"xiangmu_id":11,"xianjin":23.22,"openid":"demo_openid",'xingming':'demo_user',
                'juanzeng_shijian':datetime.now()}
        locator.add(args)
        args = {"start":0,"size":10,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}                 
        filter_args = {"openid":"demo_openid","xianjin":float(23.22)}        
        rdrs = locator.query_with_filter(args,filter_args)
        import pdb
        pdb.set_trace()
        self.assertEqual(len(rdrs),1)
        first = rdrs[0]
        # update           
        args = {"id":first.id,"openid":"test_openid"}    
        locator.updateByCode(args)
        #getByCode
        rdrs = locator.getByCode(first.id)       

        self.assertEqual(rdrs.openid,'test_openid')
        import pdb
        pdb.set_trace()
        #delete
        rt = locator.DeleteByCode(first.id)
        if rt:
            rdrs = locator.getByCode(first.id)
            self.assertEqual(rdrs,None)

    def test_AccessToken_table(self):
        from xtcs.policy.mapping_db import  AccessToken
        from xtcs.policy.interfaces import IDbapi
        from zope.component import queryUtility
        from datetime import datetime,timedelta

        locator = queryUtility(IDbapi, name='accesstoken')
        # add
        args = {"openid":"demo_openid",'token':'demo_accesstoken',
                'expiredtime':datetime.now()}
        locator.add(args)
        args = {"start":0,"size":10,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}                 
        rdrs = locator.query(args)
        self.assertEqual(len(rdrs),1)
        first = rdrs[0]
        # update           
        args = {"id":first.id,"openid":"test_openid",
                'expiredtime':datetime.now() + timedelta(hours=3)}    
        locator.updateByCode(args)
        #getByCode
        rdrs = locator.getByCode(first.id)       

        self.assertEqual(rdrs.openid,'test_openid')
        #delete
        rt = locator.DeleteByCode(first.id)
        if rt:
            rdrs = locator.getByCode(first.id)
            self.assertEqual(rdrs,None)


                
