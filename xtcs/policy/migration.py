# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
import datetime
from plone.app.contenttypes.behaviors.richtext import IRichText

from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from Acquisition import aq_parent
from plone.app.textfield.value import RichTextValue
from xtcs.policy.setuphandlers import STRUCTURE,_create_content

def create_tree(context):
    "create directory tree."
    
    # create directory structure 
    portal = api.portal.get()
    members = portal.get('events', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('news', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('Members', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject() 

    for item in STRUCTURE:
        _create_content(item, portal)    
    members = portal.get('help', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
    members = portal.get('sqls', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
       
def _create_article(article, container):
    id = str(article.id)
    new = container.get(id, None)
    if not new:
        new = api.content.create(
            type='Document',
            container=container,
            title=article.title,
            description=article.title,
            text = RichTextValue(article.content),            
            id=id,
            safe_id=False)
        datev = datetime.datetime.utcfromtimestamp(article.pubtime)
        new.setModificationDate(datev)
        new.creation_date = datev
        new.setEffectiveDate(datev)           
        new.reindexObject()         

def import_article(context):    
    "migrate articles to document"
    portal = api.portal.get()
     
    from xtcs.policy.mapping_db import  Article
    from xtcs.policy.interfaces import IArticleLocator    
    from zope.component import getUtility
    from xtcs.policy import Session as session
    locator = getUtility(IArticleLocator)
        # gongyixinwen
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1003,sortchildid=1)
        if articles == None:pass

        for article in articles:
            container =  portal['cishanzixun']['gongyixinwen']                                 
            try:
                _create_article(article,container)
            except:
                continue              

    except:
        pass
   
        # huodongtonggao
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1003,sortchildid=2)
        if articles == None:pass
        for article in articles:                                 
                  
            container = portal['cishanzixun']['huodongtonggao']
            try:
                _create_article(article,container)
            except:
                continue 
    except:
        pass    
#cishandongtai
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1003,sortchildid=3)
        if articles == None:pass
        for article in articles:                                        
            container = portal['cishanzixun']['cishandongtai']
            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass

#zhengcefagui
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1008,sortchildid=9)
        if articles == None:pass
        for article in articles:                                  
       
            container = portal['zuzhiguanli']['zhengcefagui']
            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass
    
#guizhangzhidu
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1008,sortchildid=6)
        if articles == None:pass
        for article in articles:                                  
       
            container = portal['zuzhiguanli']['guizhangzhidu']
            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass
    
#yigonghuodong
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1006,sortchildid=18)
        if articles == None:pass
        for article in articles:                                  
       
            container = portal['yigongzhongxin']['yigonghuodong']
            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass
    
#cishanwenzhai
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1007,sortchildid=20)
        if articles == None:pass
        for article in articles:                                  
   
            container = portal['cishanshequ']['cishanwenzhai']            

            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass
    
#aixingushi
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1007,sortchildid=21)
        if articles == None:pass
        for article in articles:                                  
   
            container = portal['cishanshequ']['aixingushi']           

            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass
#jingcaibowen
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1007,sortchildid=22)
        if articles == None:pass
        for article in articles:                                
     
            container = portal['cishanshequ']['jingcaibowen']            

            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass
    
#luntanretie
    try:        
        articles = locator.query(start=0,size=5,multi=1,sortparentid=1007,sortchildid=23)
        if articles == None:pass
        for article in articles:                                  
      
            container = portal['cishanshequ']['luntanretie']
            try:
                _create_article(article,container)
            except:
                continue
    except:
        pass                        