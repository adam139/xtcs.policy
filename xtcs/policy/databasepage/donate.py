#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from xtcs.policy import Session as session
from xtcs.policy.mapping_db import Donate,IDonate
from xtcs.policy.interfaces import IDonateLocator

from xtcs.policy import  _

class DonateLocator(grok.GlobalUtility):
    implements(IDonateLocator)

    def add(self,kwargs):
        """parameters db Donate table"""
        recorder = Donate()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        try:
            session.commit()
        except:
            session.rollback()
            pass

    def query(self,**kwargs):
        """以分页方式提取donate 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """

        start = int(kwargs['start'])
        size = int(kwargs['size'])
        multi = int(kwargs['multi'])
#         import pdb
#         pdb.set_trace()
        # return total num
        if multi == 1:
            if size == 0:
                nums = session.query(func.count(Donate.did)).scalar()
                return int(nums)
            else:
                recorders = session.query(Donate).\
            order_by(Donate.did).slice(start,size).all()
                
        else:
            
            if size !=0:                     
                recorders = session.query(Donate).\
            order_by(Donate.did).slice(0,size).all()
            else:
                recorders = session.query(Donate).\
            order_by(Donate.did).all()
        try:
            session.commit()
            return recorders
        except:
            session.rollback()
            pass

    def DeleteByCode(self,id):
        "delete the specify id donate recorder"

        if id != "":
            try:
                recorder = session.query(Donate).\
                from_statement(text("SELECT * FROM donate WHERE did=:id")).\
                params(did=id).one()
                session.delete(recorder)
                session.commit()
            except:
                session.rollback()
                pass
        else:
            return None

    def updateByCode(self,kwargs):
        "update the speicy id donate recorder"

        """
        session.query(User).from_statement(text("SELECT * FROM users WHERE name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users WHERE name=:name")).params(name='ed').all()
        """

        id = kwargs['did']
        if id != "":
            try:
                recorder = session.query(Donate).\
                from_statement(text("SELECT * FROM donate WHERE did=:id")).\
                params(did=id).one()
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'did']
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
                recorder = session.query(Donate).\
                from_statement(text("SELECT * FROM donate WHERE did=:id")).\
                params(did=id).one()
                return recorder
            except:
                session.rollback()
                None
        else:
            return None
