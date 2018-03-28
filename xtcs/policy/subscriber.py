#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

from dexterity.membrane.content.member import IMember
from my315ok.socialorgnization.content.governmentdepartment import IOrgnization

def getMember(context,email):
    "get member object from email"
    catalog = getToolByName(context, "portal_catalog")
    memberbrains = catalog(object_provides=IMember.__identifier__,
                               email=email)

    if len(memberbrains) == 0:return None
    return memberbrains[0].getObject()

def updateSponsorOperator(obj,event):
    "创建sponsormember对象时，触发，更新该sponsormember关联的governmentorganization的operator记录"
    
    catalog = getToolByName(obj,'portal_catalog')

    bns = catalog.unrestrictedSearchResults({'object_provides': IOrgnization.__identifier__,
                                             'id':obj.orgname})
    if bns:
        org = bns[0].getObject()
        org.operator = obj.email
        org.reindexObject()
    else:
        pass
        

def userLoginedIn(event):
    """Redirects  logged in users to getting started wizard"""  

    portal = getSite() 
    user = event.object
    if "@" not in user.getUserName():return
    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return  
    # now complile and render our expression to url

    try:
        member_url_view = getMultiAdapter((portal, request),name=u"member_url") 
        url = member_url_view()
    except Exception, e:
        logException(u'Error during user login in redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url) 