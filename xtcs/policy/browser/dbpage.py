#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope.component import getMultiAdapter
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from plone.app.contenttypes.permissions import AddDocument
from Products.CMFCore.interfaces import ISiteRoot
from plone.memoize.instance import memoize
from xtcs.policy import _
from Products.Five.browser import BrowserView
# from collective.gtags.source import TagsSourceBinder
from zope.component import getUtility
# input data view
from plone.directives import form
from z3c.form import field, button
from Products.statusmessages.interfaces import IStatusMessage
from xtcs.policy.interfaces import InputError
from xtcs.policy.interfaces import IDonateLocator,IDonorLocator
from xtcs.policy.mapping_db import IDonate,Donate,IDonor,Donor

from xtcs.policy.interfaces import IJuanzenggongshi
# update data view
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.CMFPlone.resources import add_bundle_on_request
from zExceptions import NotFound
from xtcs.policy import InputDb

grok.templatedir('templates')

class DonortableView(BrowserView):
    "捐赠金榜"
      
    @memoize
    def getMemberList(self,start=0,size=0):
        """获取捐赠结果列表"""
        
        locator = getUtility(IDonorLocator)        
        articles = locator.query(start=0,size=0,multi=0,id=7,sortchildid=3)
        if articles == None:
            return             
        return self.outputList(articles)

    def outputList(self,braindata): 
        outhtml = ""
       
        for i in braindata:

            if bool(i.goods):
                goods = i.goods
            else:
                goods= u""                        
            out = """<tr>
            <td class="title">%(title)s</td>
            <td class="item">%(money)s</td>
            <td class="goods">%(goods)s</td></tr>""" % dict(
                                            title=i.aname,
                                            money= i.money,
                                            goods=goods)           
            outhtml = "%s%s" %(outhtml ,out)
        return outhtml

# donate table
class DonateView(BrowserView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:donate_listings
    """
    @property
    def isEditable(self):
      
        return self.pm().checkPermission(permissions.ManagePortal,self.context)
    
    @property
    def isAddable(self):

        return self.pm().checkPermission(permissions.AddPortalContent,self.context)  
    @memoize
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm

    def getPathQuery(self):

        """返回 db url
        """
        query = {}
        query['path'] = "/".join(self.context.getPhysicalPath())
        return query

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = getUtility(IDonateLocator)
        recorders = locator.query(start=query['start'],size=query['size'],multi = query['multi'])
        return recorders

# donor table
class DonorView(DonateView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_ajax_juanzeng
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"

        locator = getUtility(IDonorLocator)
        recorders = locator.query(start=query['start'],\
                                  size=query['size'],multi = query['multi'],id =query['id'] )
        return recorders


class DonatedWorkflow(BrowserView):
    """
    在线捐款流程。
    view name:donated_workflow
    """
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
        add_bundle_on_request(self.request, 'donate-legacy')
    
    def get_projects(self):
        "提取系统所有公益项目"
        
        projects = ['','','','']
        return projects 

 # ajax multi-condition search relation db
class ajaxsearch(grok.View):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
    grok.context(Interface)
    grok.name('donate_ajaxsearch')
    grok.require('zope2.View')
#     grok.require('emc.project.view_projectsummary')
    
    def Datecondition(self,key):
        "构造日期搜索条件"
        end = datetime.datetime.today()
#最近一周
        if key == 1:
            start = end - datetime.timedelta(7)
#最近一月
        elif key == 2:
            start = end - datetime.timedelta(30)
#最近一年
        elif key == 3:
            start = end - datetime.timedelta(365)
#最近两年
        elif key == 4:
            start = end - datetime.timedelta(365*2)
#最近五年
        else:
            start = end - datetime.timedelta(365*5)
#            return    { "query": [start,],"range": "min" }
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition

    def searchview(self,viewname="donate_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def render(self):
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = self.searchview()
 # datadic receive front ajax post data
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        size = int(datadic['size'])      # batch search size
        id = int(datadic['id'])
        multi = int(datadic['multi'])

        origquery = {}
#         origquery['sort_on'] = sortcolumn
#         # sql db sortt_order:asc,desc
#         origquery['sort_order'] = sortdirection
#  #模糊搜索
#         if keyword != "":
#             origquery['SearchableText'] = '%'+keyword+'%'
#origquery provide  batch search
        origquery['size'] = size
        origquery['start'] = start
        origquery['id'] = id
        origquery['multi'] = multi
#totalquery  search all
        totalquery = origquery.copy()
        totalquery['size'] = 0
        totalquery['multi'] = 1
        # search all   size = 0 return numbers of recorders
        totalnum = searchview.search_multicondition(totalquery)
        resultDicLists = searchview.search_multicondition(origquery)
        del origquery
        del totalquery
#call output function
# resultDicLists like this:[(u'C7', u'\u4ed6\u7684\u624b\u673a')]
        data = self.output(start,size,totalnum, resultDicLists)      
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)

    def output(self,start,size,totalnum,resultDicLists):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if bool(self.searchview().isAddable):
            for i in resultDicLists:
                regtime = datetime.datetime.utcfromtimestamp(i.start_time)            
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-7 text-left">
                                <a class="donate" data-name="%(name)s" data-id="%(id)s" href="%(objurl)s">%(title)s</a>
                                </td>
                                <td class="col-md-2">%(regtime)s</td>
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(objurl="%s/@@donor_listings?name=%s&id=%s" % (contexturl,i.aname,i.did),
                                                name = "%s" % i.aname,                                                
                                                id = "%s" % i.did,
                                                num=str(k + 1),
                                                regtime = regtime.strftime("%Y-%m-%d"),
                                                title=i.aname,
                                                edit_url="%s/@@update_donate/%s" % (contexturl,i.did),
                                                delete_url="%s/@@delete_donate/%s" % (contexturl,i.did))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                regtime = datetime.datetime.utcfromtimestamp(i.start_time)            
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-9 text-left">
                                <a class="donate" data-name="%(name)s" data-id="%(id)s" href="%(objurl)s">%(title)s</a>
                                </td>
                                <td class="col-md-2">%(regtime)s</td>
                                </tr> """% dict(objurl="%s/@@donor_listings?name=%s&id=%s" % (contexturl,i.aname,i.did),
                                                name = "%s" % i.aname,                                                
                                                id = "%s" % i.did,
                                                num=str(k + 1),
                                                regtime = regtime.strftime("%Y-%m-%d"),
                                                title=i.aname)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class Donorajaxsearch(ajaxsearch):
    """AJAX action for search DB donor table.
    receive front end ajax transform parameters
    """

    grok.name('donor_ajaxsearch')

    def searchview(self,viewname="donor_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def render(self):
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = self.searchview()
 # datadic receive front ajax post data
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        size = int(datadic['size'])      # batch search size
        id = int(datadic['id'])
        multi = int(datadic['multi'])

        origquery = {}
#         origquery['sort_on'] = sortcolumn
#         # sql db sortt_order:asc,desc
#         origquery['sort_order'] = sortdirection
#  #模糊搜索
#         if keyword != "":
#             origquery['SearchableText'] = '%'+keyword+'%'
#origquery provide  batch search
        origquery['size'] = size
        origquery['start'] = start
        origquery['id'] = id
        origquery['multi'] = multi
#totalquery  search all
        totalquery = origquery.copy()
        totalquery['size'] = 0
        totalquery['multi'] = 1
        
        # search all   size = 0 return numbers of recorders
        totalnum = searchview.search_multicondition(totalquery)
        resultDicLists = searchview.search_multicondition(origquery)
        del origquery
        del totalquery
#call output function
# resultDicLists like this:[(u'C7', u'\u4ed6\u7684\u624b\u673a')]
        data = self.output(start,size,totalnum, resultDicLists)      
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
    
    def output(self,start,size,totalnum,resultDicLists):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if bool(self.searchview().isAddable):        
            for i in resultDicLists:
                if i.goods == None:
                    goods = ""
                else:
                    goods = i.goods
                out = """<tr class="text-left">
                                <td class="col-md-8">%(name)s</td>
                                <td class="col-md-1">%(money)s</td>
                                <td class="col-md-1">%(goods)s</td>
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(
                                            name=i.aname,
                                            money= i.money,
                                            goods= goods,
                                            edit_url="%s/@@update_donor/%s" % (contexturl,i.doid),
                                            delete_url="%s/@@delete_donor/%s" % (contexturl,i.doid))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                if i.goods == None:
                    goods = ""
                else:
                    goods = i.goods
                out = """<tr class="text-left">
                                <td class="col-md-10">%(name)s</td>
                                <td class="col-md-1">%(money)s</td>
                                <td class="col-md-1">%(goods)s</td>
                                </tr> """% dict(
                                            name=i.aname,
                                            money= i.money,
                                            goods= goods)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data

# Delete Update Input block
class DeleteDonate(form.Form):
    "delete the specify model recorder"
    implements(IPublishTraverse)
    grok.context(IJuanzenggongshi)
    grok.name('delete_donate')
    grok.require('xtcs.policy.input_db')

    label = _(u"delete donate data")
    fields = field.Fields(IDonate).omit('did')
    ignoreContext = False

    id = None
    #receive url parameters
    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()

    def getContent(self):
        # Get the model table query funcations
        locator = getUtility(IDonateLocator)
        #to do
        #fetch the pending deleting  record
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)

        # Get the model table query funcations

        #Let z3c.form do its magic
        super(DeleteDonate, self).update()


    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete model recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = getUtility(IDonateLocator)
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/donate_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donate_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donate_listings')

class InputDonate(form.Form):
    """input db donate table data
    """

    grok.context(IJuanzenggongshi)
    grok.name('input_donate')
    grok.require('xtcs.policy.input_db')
    label = _(u"Input donate data")
    fields = field.Fields(IDonate).omit('did')
    ignoreContext = True

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(InputDonate, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit donate recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = getUtility(IDonateLocator)
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/donate_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donate_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donate_listings')

class UpdateDonate(form.Form):
    """update model table row data
    """

    implements(IPublishTraverse)
    grok.context(IJuanzenggongshi)
    grok.name('update_donate')
    grok.require('xtcs.policy.input_db')

    label = _(u"update donate data")
    fields = field.Fields(IDonate).omit('did')
    ignoreContext = False
    xhdm = None
    #receive url parameters
    # reset content
    def getContent(self):
        # Get the model table query funcations
        locator = getUtility(IDonateLocator)
        # to do
        # fetch first record as sample data
        return locator.getByCode(self.id)


    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()

    def update(self):
        self.request.set('disable_border', True)

        # Let z3c.form do its magic
        super(UpdateDonate, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = getUtility(IDonateLocator)
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/donate_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donate_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donate_listings')

##发射机数据库操作
class DeleteDonor(DeleteDonate):
    "delete the specify donor recorder"

    grok.name('delete_donor')
    label = _(u"delete fa she ji data")
    fields = field.Fields(IDonor).omit('did','doid')


    id = None
    #receive url parameters
    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()

    def getContent(self):
        # Get the model table query funcations
        locator = getUtility(IDonorLocator)
        # to do
        # fetch first record as sample data
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)

        #Let z3c.form do its magic
        super(DeleteDonor, self).update()


    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete model recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = getUtility(IDonorLocator)
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/donor_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donor_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/donor_listings')


class InputDonor(InputDonate):
    """input db donor table data
    """

    grok.name('input_donor')

    label = _(u"Input fa she ji data")
    fields = field.Fields(IDonor).omit('doid')

    def update(self):
        self.request.set('disable_border', True)

        # Get the model table query funcations
#         locator = getUtility(IDonateLocator)
        # to do
        # fetch first record as sample data
#         self.screening = locator.screeningById(self.screeningId)

        # Let z3c.form do its magic
        super(InputDonor, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit model recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = getUtility(IDonorLocator)
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@donor_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@donor_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@donor_listings')


class UpdateDonor(UpdateDonate):
    """update model table row data
    """
    grok.name('update_donor')
    label = _(u"update fa she ji data")
    fields = field.Fields(IDonor).omit('doid')

    id = None
    #receive url parameters
    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()

    def getContent(self):
        # Get the model table query funcations
        locator = getUtility(IDonorLocator)
        # to do
        # fetch first record as sample data
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateDonor, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = getUtility(IDonorLocator)

        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@donor_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@donor_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@donor_listings')

##end发射机 数据库操作


