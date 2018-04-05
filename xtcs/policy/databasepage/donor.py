#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from xtcs.policy import Session as session
from xtcs.policy.mapping_db import Donor,IDonor
from xtcs.policy.interfaces import IDonorLocator

from xtcs.policy import  _

class DonorLocator(grok.GlobalUtility):
    implements(IDonorLocator)

    def add(self,kwargs):
        """parameters db Donor table"""
        recorder = Donor()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        try:
            session.commit()
        except:
            session.rollback()
            pass

    def query(self,**kwargs):
        """以分页方式提取donor 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """

        start = int(kwargs['start'])
        size = int(kwargs['size'])
        id = int(kwargs['id'])
        multi = kwargs['multi']
#         import pdb
#         pdb.set_trace()
        # return total num
        if multi == 1:
            if size == 0:
                nums = session.query(func.count(Donor.doid)).filter_by(did=id).scalar()
                return int(nums)
            else:

                size = start + size
                recorders = session.query(Donor).filter_by(did=id).\
            order_by(Donor.doid).slice(start,size).all()
                
        else:

            if size !=0:                     
                recorders = session.query(Donor).filter_by(did=id).\
            order_by(Donor.doid).slice(0,size).all()
            else:
                recorders = session.query(Donor).filter_by(did=id).\
            order_by(Donor.doid).all()
            
        try:
            session.commit()
            return recorders
        except:
            session.rollback()
            pass

    def DeleteByCode(self,id):
        "delete the specify id donor recorder"

        if id != "":
            try:
                recorder = session.query(Donor).\
                from_statement(text("SELECT * FROM donor WHERE doid=:id")).\
                params(id=id).one()
                session.delete(recorder)
                session.commit()
            except:
                session.rollback()
                pass
        else:
            return None

    def updateByCode(self,kwargs):
        "update the speicy id donor recorder"

        """
        session.query(User).from_statement(text("SELECT * FROM users WHERE name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users WHERE name=:name")).params(name='ed').all()
        """

        id = kwargs['id']
        if id != "":
            try:
                recorder = session.query(Donor).\
                from_statement(text("SELECT * FROM donor WHERE doid=:id")).\
                params(id=id).one()
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'doid']
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
                recorder = session.query(Donor).\
                from_statement(text("SELECT * FROM donor WHERE doid=:id")).\
                params(id=id).one()
                return recorder
            except:
                session.rollback()
                None
        else:
            return None
