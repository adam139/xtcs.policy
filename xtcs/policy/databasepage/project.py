#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from xtcs.policy import Session as session
from xtcs.policy.mapping_db import Project,IProject
from xtcs.policy.interfaces import IProjectLocator

from xtcs.policy import  _

class ProjectLocator(grok.GlobalUtility):
    implements(IProjectLocator)

    def add(self,kwargs):
        """parameters db Project table"""
        recorder = Project()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        try:
            session.commit()
        except:
            session.rollback()
            pass

    def query(self,**kwargs):
        """以分页方式提取project 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """

        start = int(kwargs['start'])
        size = int(kwargs['size'])
        multi = kwargs['multi']
#         import pdb
#         pdb.set_trace()
        if multi == 1:            
            sortparentid = kwargs['sortparentid']
            sortchildid = kwargs['sortchildid']
            recorders = session.query(Project).order_by(Project.id).all()
                        
        else:
            if size != 0:
                stmt = text("select * from project order by id desc limit :start :size")
                stmt = stmt.columns(Project.title,Project.pubtime,Project.content)
                recorders = session.query(Project).from_statement(stmt).\
                params(start=start,size=size).all()
                
            else:
                nums = session.query(func.count(Project.id)).scalar()
                return int(nums)
        try:
            session.commit()
            return recorders
        except:
            session.rollback()
            pass

    def DeleteByCode(self,id):
        "delete the specify id project recorder"

        if id != "":
            try:
                recorder = session.query(Project).\
                from_statement(text("SELECT * FROM project WHERE id=:id")).\
                params(id=id).one()
                session.delete(recorder)
                session.commit()
            except:
                session.rollback()
                pass
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

        id = kwargs['id']
        if id != "":
            try:
                recorder = session.query(Project).\
                from_statement(text("SELECT * FROM project WHERE id=:id")).\
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
                recorder = session.query(Project).\
                from_statement(text("SELECT * FROM project WHERE id=:id")).\
                params(id=id).one()
                return recorder
            except:
                session.rollback()
                None
        else:
            return None
