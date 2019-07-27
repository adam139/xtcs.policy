# -*- coding: UTF-8 -*-
from datetime import datetime
from five import grok
# sqlarchemy
from sqlalchemy import func
from sqlalchemy import text
from xtcs.policy import _
from xtcs.policy import maintan_session
from xtcs.policy import Scope_session
from xtcs.policy.interfaces import IVolunteerteamLocator
from xtcs.policy.mapping_db import IVolunteerteam
from xtcs.policy.mapping_db import Volunteerteam
from zope import schema
from zope.interface import implements


class VolunteerteamLocator(grok.GlobalUtility):
    implements(IVolunteerteamLocator)

    def add(self, kwargs):
        """parameters db Volunteerteam table"""
        session = Scope_session()
        recorder = Volunteerteam()
        for kw in kwargs.keys():
            setattr(recorder, kw, kwargs[kw])
        session.add(recorder)
        maintan_session(session)

    def query(self, **kwargs):
        """以分页方式提取project 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """

        session = Scope_session()
        start = int(kwargs['start'])
        size = int(kwargs['size'])
#         id = int(kwargs['id'])
        multi = kwargs['multi']
        # return total num
        if multi == 1:
            if size == 0:
                nums = session.query(func.count(Volunteerteam.id)).scalar()
                return int(nums)
            else:

                size = start + size
                recorders = session.query(Volunteerteam).\
                    order_by(Volunteerteam.id).slice(start, size).all()

        else:

            if size != 0:
                recorders = session.query(Volunteerteam).\
                    order_by(Volunteerteam.id).slice(0, size).all()
            else:
                recorders = session.query(Volunteerteam).\
                    order_by(Volunteerteam.id).all()
        maintan_session(session)
        return recorders

    def DeleteByCode(self, id):
        "delete the specify id project recorder"

        session = Scope_session()
        if id != "":
            recorder = session.query(Volunteerteam).\
                from_statement(text("SELECT * FROM volunteerteam WHERE id=:id")).\
                params(id=id).one()
            session.delete(recorder)
            maintan_session(session)
        else:
            return None

    def updateByCode(self, kwargs):
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
            recorder = session.query(Volunteerteam).\
                from_statement(text("SELECT * FROM volunteerteam WHERE id=:id")).\
                params(id=id).one()
            updatedattrs = [kw for kw in kwargs.keys() if kw != 'id']
            for kw in updatedattrs:
                setattr(recorder, kw, kwargs[kw])
            maintan_session(session)
        else:
            return None

    def getByCode(self, id):
        session = Scope_session()
        if id != "":
            recorder = session.query(Volunteerteam).\
                from_statement(text("SELECT * FROM volunteerteam WHERE id=:id")).\
                params(id=id).one()
            maintan_session(session)
            return recorder
        else:
            return None
