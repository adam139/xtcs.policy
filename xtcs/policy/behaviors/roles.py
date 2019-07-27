# -*- coding: utf-8 -*-
from dexterity.membrane.behavior.membraneuser import DxUserObject
from dexterity.membrane.behavior.membraneuser import IMembraneUser
from dexterity.membrane.content.member import IOrganizationMember
from dexterity.membrane.content.member import ISponsorMember
from Products.membrane.interfaces import IMembraneUserRoles
from zope.component import adapter
from zope.interface import implementer


DEFAULT_ORG_ROLES = ['Social Organization', 'Reviewer']
DEFAULT_SPR_ROLES = ['Sponsor', 'Reviewer']


@implementer(IMembraneUserRoles)
@adapter(IOrganizationMember)
class OrgDefaultRoles(DxUserObject):

    def getRolesForPrincipal(self, principal, request=None):
        return DEFAULT_ORG_ROLES


@implementer(IMembraneUserRoles)
@adapter(ISponsorMember)
class SprDefaultRoles(DxUserObject):

    def getRolesForPrincipal(self, principal, request=None):
        return DEFAULT_SPR_ROLES
