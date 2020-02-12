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

#     def test_article_get(self):
#         from xtcs.policy.mapping_db import  Article
#         from xtcs.policy.interfaces import IArticleLocator
#         from zope.component import getUtility
#         from xtcs.policy import Session as session
# 
#         locator = getUtility(IArticleLocator)
#         #getModel
#         id = 200
#         title = u"test article"
#         pubtime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         content = u"<p>test article</p>"
#         sortparentid = 2018
#         sortchildid = 1        
#         article = locator.getByCode(id)
#         #addModel
# 
#         if article == None:
#             locator.add(id=id,title=title,pubtime=pubtime,content= content)
#         else:
#             # remove old  delete
#             locator.DeleteByCode(id)
#             locator.add(id=id,title=title,pubtime=pubtime,content= content)
# 
#         article = locator.getByCode(id)
#         self.assertEqual(article.id,id)
#         # query pagenation 分页查询
#         articles = locator.query(start=0,size=1,id=id)
# 
#         self.assertEqual(len(articles),1)

    def test_article_query(self):
        from xtcs.policy.mapping_db import  Article
        from xtcs.policy.interfaces import IArticleLocator
        from zope.component import getUtility
        from xtcs.policy import Session as session

        locator = getUtility(IArticleLocator)        
        articles = locator.query(start=0,size=10,multi=1,sortparentid=1003,sortchildid=3)
        if articles == None:
            return
        import pdb
        pdb.set_trace()
        self.assertEqual(len(articles),10)

    def test_import_article(self):
        from xtcs.policy.mapping_db import  Article
        from xtcs.policy.interfaces import IArticleLocator
        from zope.component import getUtility

        locator = getUtility(IArticleLocator)
        articles = locator.query(start=0,size=3,multi=1,sortparentid=1003,sortchildid=3)
        if articles == None:return

        for article in articles:                                  
            docid = str(article.id)      
            container=self.portal['cishanzixun']['cishandongtai']
            _create_article(article,container)
            document = self.portal['cishanzixun']['cishandongtai'][docid]

            self.request.set('URL', document.absolute_url())
            self.request.set('ACTUAL_URL', document.absolute_url())
            alsoProvides(self.request, IPloneFormLayer)
            view = document.restrictedTraverse('@@view')
            self.assertEqual(view.request.response.status, 200)
            output = view()
            self.assertTrue(output)
#         self.assertTrue('My Document' in output)
#             self.assertTrue('This is my document.' in output)
#         self.assertTrue('Lorem ipsum' in output)

    def test_article_pubtime(self):

        from xtcs.policy.interfaces import IArticleLocator
        from zope.component import getUtility
        locator = getUtility(IArticleLocator)
        articles = locator.query(start=0,size=1,multi=1,sortparentid=1003,sortchildid=3)
        if articles == None:return
        container = self.portal['cishanzixun']['cishandongtai']
        for article in articles:                                  
            _create_article(article,container)
            doc = container[str(article.id)]
            pubtime = datetime.datetime.utcfromtimestamp(article.pubtime)
            self.assertTrue(doc.created().strftime("Y-%m-%d") == pubtime.strftime("Y-%m-%d"))
            
    def tearDown(self):
        if 'document' in self.portal.objectIds():
            self.portal.manage_delObjects(ids='document')
            transaction.commit()

    def test_project_query(self):
        from xtcs.policy.mapping_db import  Project
        from xtcs.policy.interfaces import IProjectLocator
        from zope.component import getUtility
        from xtcs.policy import Session as session

        locator = getUtility(IProjectLocator)        
        articles = locator.query(start=0,size=100,multi=1,sortparentid=1003,id=3)
        if articles == None:
            return
        self.assertEqual(len(articles),3)

    def test_Donor_table(self):
        from xtcs.policy.mapping_db import  Donor
        from xtcs.policy.interfaces import IDbapi
        from zope.component import getUtility,queryUtility

        locator = queryUtility(IDbapi, name='donor')
        # add
        args = {"did":21,"aname":"demo user2",'googds':'testgoods'}
        locator.add(args)        
        # batch search
        args = {"start":0,"size":10,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'doid'}
        filter_args = {"did":21}        
        rdrs = locator.query_with_filter(args,filter_args)
        self.assertEqual(len(rdrs),10)
        # fulltext batch search        
        args = {"start":0,"size":10,'SearchableText':'demo',
                'with_entities':0,'sort_order':'reverse','order_by':'doid'}
        filter_args = {"did":21}        
        rdrs2 = locator.query_with_filter(args,filter_args)
        self.assertEqual(len(rdrs2),1)
        first = rdrs[0]
        # update           
        args = {"id":first.doid,"pk":"doid",'aname':'demo user'}    
        locator.updateByCode(args)
        #getByCode
        rdrs = locator.getByCode(first.doid,"doid")       

        self.assertEqual(rdrs.aname,'demo user')
        #delete
        rt = locator.DeleteByCode(first.doid,"doid")
        if rt:
            rdrs = locator.getByCode(first.doid,"doid")
            self.assertEqual(rdrs,None)
            
    def test_Donate_table(self):
        from xtcs.policy.mapping_db import  Donate
        from xtcs.policy.interfaces import IDbapi
        from zope.component import getUtility,queryUtility
        from datetime import datetime

        locator = queryUtility(IDbapi, name='donate')
        # add
        fmt = "%Y-%m-%d %H:%M:%S"
        import time
        now = datetime.now()
        dtst = time.strptime(now.strftime(fmt),fmt)
        timestamp = int(time.mktime(dtst))
        args = {"aname":"demo project",'visible':1,'start_time':timestamp}
#         locator.add(args)        
        # batch search
        args = {"start":0,"size":3,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'did'}
      
        rdrs = locator.query(args)
        self.assertEqual(len(rdrs),3)
        # fulltext batch search        
        args = {"start":0,"size":10,'SearchableText':'demo',
                'with_entities':0,'sort_order':'reverse','order_by':'did'}
       
        rdrs2 = locator.query(args)
        self.assertEqual(len(rdrs2),2)
        first = rdrs[0]
        # update           
        args = {"id":first.did,"pk":"did",'aname':'demo user'}    
        locator.updateByCode(args)
        #getByCode
        rdrs = locator.getByCode(first.did,"did")       

        self.assertEqual(rdrs.aname,'demo user')
        #delete
        rt = locator.DeleteByCode(first.did,"did")
        if rt:
            rdrs = locator.getByCode(first.did,"did")
            self.assertEqual(rdrs,None)
                

    def test_donate_query(self):

        from xtcs.policy.interfaces import IDonateLocator
        from zope.component import getUtility


        locator = getUtility(IDonateLocator)
        
        articles = locator.query(start=0,size=100,multi=1,did=18,sortchildid=3)
        if articles == None:
            return
        self.assertEqual(len(articles),4)

    def test_volunteerteam_query(self):
        from xtcs.policy.mapping_db import  Volunteerteam
        from xtcs.policy.interfaces import IVolunteerteamLocator
        from zope.component import getUtility
        from xtcs.policy import Session as session

        locator = getUtility(IVolunteerteamLocator)
        
        articles = locator.query(start=0,size=100,multi=1,did=18,id=2)
        if articles == None:
            return
        self.assertEqual(len(articles),2)


