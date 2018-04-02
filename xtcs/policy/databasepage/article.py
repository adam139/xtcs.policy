#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from xtcs.policy import Session as session
from xtcs.policy.mapping_db import Article,IArticle
from xtcs.policy.interfaces import IArticleLocator

from xtcs.policy import  _

class ArticleLocator(grok.GlobalUtility):
    implements(IArticleLocator)

    def add(self,kwargs):
        """parameters db Article table"""
        recorder = Article()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        try:
            session.commit()
        except:
            session.rollback()
            pass

    def query(self,**kwargs):
        """以分页方式提取article 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """

        start = int(kwargs['start'])
        size = int(kwargs['size'])
        multi = kwargs['multi']

        # return total num
        if multi == 1:
            if size == 0:
                nums = session.query(func.count(Article.id)).scalar()
                return int(nums)
            else:
                sortchildid = kwargs['sortchildid']
                recorders = session.query(Article).filter_by(sortchildid=sortchildid).\
            order_by(Article.id).slice(start,size).all()
                
        else:
            sortchildid = kwargs['sortchildid']
            if size !=0:                     
                recorders = session.query(Article).filter_by(sortchildid=sortchildid).\
            order_by(Article.id).slice(0,size).all()
            else:
                recorders = session.query(Article).filter_by(sortchildid=sortchildid).\
            order_by(Article.id).all()

        try:
            session.commit()
            return recorders
        except:
            session.rollback()
            pass

    def DeleteByCode(self,id):
        "delete the specify id article recorder"

        if id != "":
            try:
                recorder = session.query(Article).\
                from_statement(text("SELECT * FROM article WHERE id=:id")).\
                params(id=id).one()
                session.delete(recorder)
                session.commit()
            except:
                session.rollback()
                pass
        else:
            return None

    def updateByCode(self,kwargs):
        "update the speicy id article recorder"

        """
        session.query(User).from_statement(text("SELECT * FROM users WHERE name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users WHERE name=:name")).params(name='ed').all()
        """

        id = kwargs['id']
        if id != "":
            try:
                recorder = session.query(Article).\
                from_statement(text("SELECT * FROM article WHERE id=:id")).\
                params(id=id).one()
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'id']
                for kw in updatedattrs:
                    setattr(recorder,kw,kwargs[kw])
                session.commit()
            except:
                session.rollback()
                pass
        else:
            return None

    def getByCode(self,id):
        if id != "":
#             import pdb
#             pdb.set_trace()
            try:
                recorder = session.query(Article).\
                from_statement(text("SELECT * FROM article WHERE id=:id")).\
                params(id=id).one()
                return recorder
            except:
                session.rollback()
                None
        else:
            return None
