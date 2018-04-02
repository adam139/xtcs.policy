# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer

from plone.app.contenttypes.behaviors.richtext import IRichText

from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from Acquisition import aq_parent
from plone.app.textfield.value import RichTextValue
from xtcs.policy.setuphandlers import STRUCTURE,_create_content 

def import_article(context):
    "import article from mysql to plone."
    
    # migrate articles to document
    # 
# sortparenid:1002:慈善资讯
# sortchildid:1:公益新闻
# sortchildid:2:活动通知
# sortchildid:3:慈善动态
# sortparenid:1006:义工中心
# sortchildid:18:义工活动
# sortparenid:1007:慈善社区
# sortchildid:20:慈善文摘
# sortchildid:21:慈善故事
# sortchildid:22:精彩博文
# sortchildid:23:论坛热铁
# sortparenid:1008:组织管理
# sortchildid:6:规章制度
# sortchildid:9:政策法规    
    from xtcs.policy.mapping_db import  Article
    from xtcs.policy.interfaces import IArticleLocator
    
    from zope.component import getUtility
    from xtcs.policy import Session as session

    
    def _create_doc(article):
        portal = api.portal.get()
        try:
            container = portal['cishanzixun']['cishandongtai']
            new = container.get(str(sourceObj.id), None)
            if not new:
                new = api.content.create(
                                     type='Document',
                                     container=container,
                                     title=article.title,
                                     description=article.title,            
                                     id=str(article.id),
                                     safe_id=False)
                datev = datetime.datetime.utcfromtimestamp(article.pubtime)
                if new != None:
                    new.text = RichTextValue(article.content)
                    new.setModificationDate(datev)
                    new.creation_date = datev
                    new.setEffectiveDate(datev)
                    new.reindexObject(idxs=['created', 'modified','Title'])        
        except:
            pass
    #慈善动态
    portal = api.portal.get()
#     catalog = api.portal.get_tool(name='portal_catalog')
    try:
        container = portal['cishanzixun']['cishandongtai']
        if container != None:
            locator = getUtility(IArticleLocator)    
            articles = locator.query(start=0,size=100,multi=1,sortparentid=1003,sortchildid=3)
            finished = map(_create_doc,articles)
        else:
            pass
    except:
       pass


   
    


