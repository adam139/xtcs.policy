#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from xtcs.policy import Scope_session,maintan_session
from xtcs.policy.mapping_db import Donate,IDonate
from xtcs.policy.interfaces import IDonateLocator

from xtcs.policy import  _

class DonateLocator(grok.GlobalUtility):
    implements(IDonateLocator)

    def add(self,kwargs):
        """parameters db Donate table"""
        session = Scope_session()
        recorder = Donate()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        maintan_session(session)

    def query(self,**kwargs):
        """以分页方式提取donate 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """

        session = Scope_session()
        start = int(kwargs['start'])
        size = int(kwargs['size'])
        multi = int(kwargs['multi'])
        if multi == 1:
            if size == 0:
                nums = session.query(func.count(Donate.did)).scalar()
                return int(nums)
            else:
                recorders = session.query(Donate).\
            order_by(Donate.did.desc()).slice(start,size).all()
                
        else:            
            if size !=0:                     
                recorders = session.query(Donate).\
            order_by(Donate.did.desc()).slice(0,size).all()
            else:
                recorders = session.query(Donate).\
            order_by(Donate.did.desc()).all()
            
        maintan_session(session)
        return recorders

    def DeleteByCode(self,id):
        "delete the specify id donate recorder"

        session = Scope_session()
        if id != "":

            recorder = session.query(Donate).filter(Donate.did ==id).one()
            session.delete(recorder)
            maintan_session(session)
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

        session = Scope_session()
        id = kwargs['did']
        if id != "":
            recorder = session.query(Donate).filter(Donate.did ==id).one()
            updatedattrs = [kw for kw in kwargs.keys() if kw != 'did']
            for kw in updatedattrs:
                setattr(recorder,kw,kwargs[kw])
            maintan_session(session)
        else:
            return None

    def getByCode(self,id):
        session = Scope_session()
#         import pdb
#         pdb.set_trace()
        if id != "":
            recorder = session.query(Donate).filter(Donate.did ==id).one()
            maintan_session(session)
            return recorder
        else:
            return None
