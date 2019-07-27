# -*- coding: utf-8 -*-
from dexterity.membrane.content.member import IOrganizationMember
from dexterity.membrane.content.member import ISponsorMember
from my315ok.socialorgnization.content.orgnization import IOrgnization
from Products.CMFCore.utils import getToolByName
from xtcs.policy import MessageFactory as _
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class IOrg(Interface):

    def getOrgBn():
        """get relative organization brain
        """
    def getLegalPerson():
        """ 获取法人"""

    def getSponsor():
        """获取监管单位
        """


@implementer(IOrg)
@adapter(IOrganizationMember)
class Org(object):
    """member adapter"""

    def __init__(self, context):
        self.context = context

    def getOrgBn(self):
        "get sponsor"
        orgid = self.context.orgname
        if not orgid:
            return None
        catalog = getToolByName(self.context, "portal_catalog")
        query = {"object_provides": IOrgnization.__identifier__, 'id': orgid}
        bs = catalog(query)
        return bs[0]

    def getOrgPath(self):
        bn = self.getOrgBn()
        if bn:
            return bn.getURL()
        return None

    def getLegalPerson(self):
        bn = self.getOrgBn()
        if bn:
            return bn.orgnization_legalPerson
        return ""

    def getSponsor(self):
        bn = self.getOrgBn()
        if bn:
            return bn.orgnization_supervisor
        return ""


class ISponsor(Interface):
    "adapte ISponsorMember to support this interface"

    def getSponsorBn():
        """get relative organization brain
        """


@implementer(ISponsor)
@adapter(ISponsorMember)
class Sponsor(object):
    """member adapter,adapte ISponsorMember to support ISponsor"""

    def __init__(self, context):
        self.context = context

    def getSponsorBn(self):
        "get sponsor"
        from my315ok.socialorgnization.content.governmentdepartment import IOrgnization
        orgid = self.context.orgname
        if not orgid:
            return None
        catalog = getToolByName(self.context, "portal_catalog")
        query = {"object_provides": IOrgnization.__identifier__, 'id': orgid}
        bs = catalog(query)
        return bs[0]
