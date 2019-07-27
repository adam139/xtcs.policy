# -*- coding: utf-8 -*-
from plone.app.content.interfaces import INameFromTitle
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import datetime


class INameFromYear(Interface):
    """ Interface to adapt to INameFromTitle """


class INameFromAdminYear(Interface):
    """ Interface to adapt to INameFromTitle for administrative licence object"""


@implementer(INameFromTitle)
@adapter(INameFromYear)
class NameFromYear(object):
    """ Adapter to INameFromTitle """

    def __init__(self, context):
        pass

    def __new__(cls, context):
        #        org = context.brand
        year = (datetime.datetime.today() +
                datetime.timedelta(-365)).strftime("%Y")
        title = u'%s' % (year)
        inst = super(NameFromYear, cls).__new__(cls)
        inst.title = title
        return inst


@implementer(INameFromTitle)
@adapter(INameFromAdminYear)
class NameFromAdminYear(object):
    """ Adapter to INameFromTitle """

    def __init__(self, context):
        pass

    def __new__(cls, context):
        #        org = context.brand
        now = datetime.datetime.today()
        year = now.strftime("%Y")
        day = now.strftime("%d")
        title = u'admin_%s_%s' % (year, day)
        inst = super(NameFromAdminYear, cls).__new__(cls)
        inst.title = title
#        context.setTitle(title)
        return inst
