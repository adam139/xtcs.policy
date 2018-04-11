#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from xtcs.policy import Scope_session,maintan_session
from xtcs.policy.mapping_db import Project,IProject
from xtcs.policy.interfaces import IProjectLocator

from xtcs.policy import  _

class ProjectLocator(grok.GlobalUtility):
    implements(IProjectLocator)

    def add(self,kwargs):
        """parameters db Project table"""
        session = Scope_session()        
        recorder = Project()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])

        session.add(recorder)
        maintan_session(session)

    def query(self,**kwargs):
        """以分页方式提取project 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """
        session = Scope_session()
        start = int(kwargs['start'])
        size = int(kwargs['size'])
        id = int(kwargs['id'])
        multi = kwargs['multi']
#         import pdb
#         pdb.set_trace()
        # return total num
        if multi == 1:
            if size == 0:
                nums = session.query(func.count(Project.id)).scalar()
                return int(nums)
            else:

                size = start + size
                recorders = session.query(Project).\
            order_by(Project.id).slice(start,size).all()
                
        else:

            if size !=0:                     
                recorders = session.query(Project).\
            order_by(Project.id).slice(0,size).all()
            else:
                recorders = session.query(Project).\
            order_by(Project.id).all()
            
        maintan_session(session)
        return recorders

    def DeleteByCode(self,id):
        "delete the specify id project recorder"

        session = Scope_session()        
        if id != "":

            recorder = session.query(Project).\
                from_statement(text("SELECT * FROM project WHERE id=:id")).\
                params(id=id).one()
            session.delete(recorder)
            maintan_session(session)
        else:
            return None

    def updateByCode(self,kwargs):
        "update the speicy id project recorder"

        """
        session.query(User).from_statement(text("SELECT * FROM users WHERE name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users WHERE name=:name")).params(name='ed').all()
        """
        session = Scope_session() 
        id = kwargs['id']
        if id != "":
            recorder = session.query(Project).\
                from_statement(text("SELECT * FROM project WHERE id=:id")).\
                params(id=id).one()
            updatedattrs = [kw for kw in kwargs.keys() if kw != 'id']
            for kw in updatedattrs:
                setattr(recorder,kw,kwargs[kw])
            maintan_session(session)
        else:
            return None

    def getByCode(self,id):
        session = Scope_session()        
        if id != "":
            recorder = session.query(Project).\
                from_statement(text("SELECT * FROM project WHERE id=:id")).\
                params(id=id).one()
            maintan_session(session)
            return recorder
        else:
            return None
