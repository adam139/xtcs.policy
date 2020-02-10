#-*- coding: UTF-8 -*-
from __future__ import division
from plone import api
from zope.interface import Interface
from zope.component import getMultiAdapter
from five import grok
import json
from datetime import date
import time
from datetime import datetime
from datetime import timedelta
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from xtcs.policy.browser.interfaces import IwechatSettings
fmt = "%Y-%m-%d %H:%M:%S"
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from plone.app.contenttypes.permissions import AddDocument
from Products.CMFCore.interfaces import ISiteRoot
from plone.memoize.instance import memoize
from xtcs.policy import _
from Products.Five.browser import BrowserView
# from collective.gtags.source import TagsSourceBinder
from zope.component import getUtility,queryUtility
# input data view
from plone.directives import form
from z3c.form import field, button
from Products.statusmessages.interfaces import IStatusMessage
from xtcs.policy.interfaces import InputError,IDbapi
from xtcs.policy.interfaces import IDonateLocator,IDonorLocator
from xtcs.policy.mapping_db import IDonate,Donate,IDonor,Donor
from xtcs.policy.mapping_db import OnlinePay
from xtcs.policy import Scope_session as Session

from xtcs.policy.interfaces import IJuanzenggongshi
from my315ok.wechat.pay import WeixinHelper
from my315ok.wechat.pay import UnifiedOrder_pub
from my315ok.wechat.pay import JsApi_pub
from my315ok.wechat.pay import Wxpay_server_pub
from my315ok.wechat.pay import OrderQuery_pub
from my315ok.wechat.pay import WxPayConf_pub
from my315ok.wechat.lib import HttpClient 
# update data view
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.CMFPlone.resources import add_bundle_on_request
from zExceptions import NotFound
from xtcs.policy import InputDb
import logging
logger = logging.getLogger("weixin notify")

# our helper class
class CustomWeixinHelper(WeixinHelper):
    "overrite get access token method for cached and refresh"
    
    @classmethod
    def getAccessToken(cls):
        """获取access_token
        需要缓存access_token,由于缓存方式各种各样，不在此提供
        http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
        """
        logger.info("enter get accesstoken")
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        stime = settings.access_token_time
        token = settings.access_token
        logger.info("old token is:%s,old time is:%s" % (token,stime))
        if bool(token) and stime + timedelta(seconds=7000) > datetime.now():
            return token        
        _ACCESS_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
        token = HttpClient().get(_ACCESS_URL.format(WxPayConf_pub.APPID, WxPayConf_pub.APPSECRET))
        logger.info("new token is:%s" % token)
        if 'errcode' not in token.keys(): 
            settings.access_token_time = datetime.now()
            settings.access_token = token['access_token']
        return token['access_token']


    @classmethod
    def getAccessTokenByCode(cls, code):
        """通过code换取网页授权access_token, 该access_token与getAccessToken()返回是不一样的
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """

        logger.info("enter getAccessTokenByCode. code:'%s'" % code)
        
        token = WeixinHelper.getAccessTokenByCode(code)
        if 'errcode' not in token.keys():
            #refresh access_token
            token = WeixinHelper.refreshAccessToken(token['refresh_token'])
        logger.info("new refresh token is:%s" % token)       
        return token

    @classmethod
    def getJsapiTicket(cls, access_token):
        """获取jsapi_ticket
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)        
        stime = settings.jsapi_ticket_time
        ticket = settings.jsapi_ticket
        if bool(ticket) and stime + timedelta(seconds=7000) > datetime.now():
            return token         
        _JSAPI_URL = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi"
        ticket = HttpClient().get(_JSAPI_URL.format(access_token))
        settings.jsapi_ticket_time = datetime.now()
        settings.jsapi_ticket = ticket         
        return ticket
    


grok.templatedir('templates')

class DonortableView(BrowserView):
    "捐赠金榜,显示日常捐赠"
      
    @memoize
    def getMemberList(self,start=0,size=0):
        """获取捐赠结果列表"""
        
        locator = getUtility(IDonorLocator)        
        articles = locator.query(start=0,size=0,multi=0,id=21,sortchildid=3)
        if articles == None:
            return             
        return self.outputList(articles)

    def outputList(self,braindata): 
        outhtml = ""
       
        for i in braindata:
            astr = i.atime.strftime('%Y-%m-%d')
            if astr != '2000-01-01':
                atime = astr
            else:
                atime= u""                        
            if bool(i.goods):
                if bool(i.money):
                    money = "%s(%s)" % (i.money,i.goods)
                else:
                    money = "(%s)" % (i.goods)
            else:
                money = i.money            
            out = """<tr>
            <td class="title">%(title)s</td>
            <td class="item">%(money)s</td>
            <td class="atime">%(atime)s</td></tr>""" % dict(
                                            title=i.aname,
                                            money= money,
                                            atime=atime)           
            outhtml = "%s%s" %(outhtml ,out)
        return outhtml

class GuanZhuangDonortableView(DonortableView):
    "冠状疫情捐赠"
      
    @memoize
    def getMemberList(self,start=0,size=0):
        """获取捐赠结果列表"""
        
        locator = getUtility(IDonorLocator)        
        articles = locator.query(start=0,size=0,multi=0,id=22,sortchildid=3)
        if articles == None:
            return             
        return self.outputList(articles)

# all donate table
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

class SpecifyDonorView(DonorView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，并提供表id,查询数据库的日常捐赠表,并返回结果。
    
    parameters:
        query:{'start':0,'size':10}
        id:21
    view name:db_ajax_juanzeng
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"

        locator = getUtility(IDonorLocator)
        recorders = locator.query(start=query['start'],\
                                  size=query['size'],multi = query['multi'],id=21 )
        return recorders


class GuangZhuangDonorView(DonorView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，并提供表id,查询数据库的日常捐赠表,并返回结果。
    
    parameters:
        query:{'start':0,'size':10}
        id:21
    view name:db_ajax_juanzeng
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"

        locator = getUtility(IDonorLocator)
        recorders = locator.query(start=query['start'],\
                                  size=query['size'],multi = query['multi'],id=22 )
        return recorders



class WeixinPay(BrowserView):
    """
    在线捐款流程。
    view name:donated_workflow
    """
    def get_auth_page(self):
        ""
        return "@@auth"
    
    def get_projects(self,id=None):
        "提取系统所有公益项目"

        query = {'start':0,'size':10,'multi':0}      
        locator = getUtility(IDonateLocator)
        recorders = locator.multi_query(start=query['start'],size=query['size'],multi = query['multi'])

        def outfmt(rcd):
            out = '<label><input type="radio" name="{0}" id="{1}" value="{2}">{3}</label>'
            name = "project{0}".format(rcd.did)
            out = out.format("project",name,rcd.did,rcd.aname)
            return out
            
        outhtml = map(outfmt,recorders)
        if bool(outhtml):
            first = outhtml[0]
            index = first.find('value') 
            outhtml[0] = first[:index] + ' checked ' + first[index:]
             
        outhtml = "<br/>".join(outhtml)
        return outhtml

class CurrentWeixinPay(WeixinPay):
    """
    在线捐款流程。
    view name:donated_workflow
    """
    def get_projects(self,id):
        "提取当前公益项目,id is project id"
        locator = getUtility(IDonateLocator)
        rcd = locator.getByCode(id)
        out = dict()
        out['title'] = rcd.aname
        st = '<label><input type="radio" name="{0}" id="{1}" value="{2}" checked>{3}</label>'
        pid = "project{0}".format(rcd.did)
        out['html']  = st.format("project",pid ,rcd.did,rcd.aname)
        return out
        

        
    
class DonatedWorkflow(WeixinPay):
    """
    在线捐款流程。
    view name:donated_workflow
    """
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
        add_bundle_on_request(self.request, 'donate-legacy')    
       

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
        end = datetime.today()
#最近一周
        if key == 1:
            start = end - timedelta(7)
#最近一月
        elif key == 2:
            start = end - timedelta(30)
#最近一年
        elif key == 3:
            start = end - timedelta(365)
#最近两年
        elif key == 4:
            start = end - timedelta(365*2)
#最近五年
        else:
            start = end - timedelta(365*5)
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
                regtime = datetime.utcfromtimestamp(i.start_time)            
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
                regtime = datetime.utcfromtimestamp(i.start_time)            
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


class TokenAjax(grok.View):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
    grok.context(Interface)
    grok.name('token_ajax')
    grok.require('zope2.View')

    def getAccessTokenByCode(self):
        
        try:
            code = self.request.form['code']      
            token = WeixinHelper.getAccessTokenByCode(code)
            return token
        except:
            return ""
        
    
    def render(self):
        "response to front end"       
    
        token = self.getAccessTokenByCode()
        self.request.response.setHeader('Content-Type', 'application/json')
        return token        
            

# class NotifyAjax(grok.View,Wxpay_server_pub):

class NotifyAjax(object):    
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def __call__(self):
        """weixin callback"""        
        logger.info("weixin callback ------entering !")
        if self.request['method'] == 'GET':
            logger.info("received get quest=get !")
            self.request.response.setHeader('Content-Type', 'application/xml')          
            return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"

        base = Wxpay_server_pub()     
        datadic = self.request['xml']
        logger.info(str(datadic))
#         api = CustomCustomWeixinHelper()     
        datadic = WeixinHelper.xmlToArray(datadic)
        openid = datadic['openid']
        money =  datadic['total_fee']        
        money = int(money)/100  
        base.data = datadic
        locator = queryUtility(IDbapi, name='onlinepay')
        # 验证签名和金额是否一致 金额在用户下单插入数据库
#         recorder = locator.getByKwargs(openid=openid,money=money)
        recorder = Session.query(OnlinePay).filter(OnlinePay.openid==openid).\
            filter(OnlinePay.money==str(money)).order_by(OnlinePay.id.desc()).first() 
        
        if base.checkSign() and bool(recorder):            
            # update status=1
            locator.updateByCode({"id":recorder.id,"status":1})
            out = 'ok'
            # send template message
            
            message = u"湘潭市慈善总会于:{0},收到您的捐款:{1}元,感谢您的善心善行!"
            nw = datetime.now().strftime(fmt)
            logger.info("start send text message:%s" % message.format(nw,money))
            access_token = CustomWeixinHelper.getAccessToken()
            logger.info("base accesstoken:%s" % access_token)
            WeixinHelper.sendTextMessage(openid, message.format(nw,money), access_token)

        else:            
            out = 'no'        
        self.request.response.setHeader('Content-Type', 'text/plain')        
        return out               


class SuccessNotifyAjax(object):    
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def __call__(self):
        """weixin callback"""
        
        datadic = self.request.form 
        trade_no = datadic['out_trade_no']
        t_id = datadic['transaction_id']        
        if datadic["result"] == "ok":
            # query order
            qapi = OrderQuery_pub()
            qapi.parameters['out_trade_no'] = trade_no
            qapi.parameters['transaction_id'] = t_id
            result = qapi.getResult()            
            out = {"result":"yes"}
        else:
            out = {"result":"no"}
        self.request.response.setHeader('Content-Type', 'application/json')
        return out
 

class PayAjax(grok.View):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
    grok.context(Interface)
    grok.name('pay_ajax')
    grok.require('zope2.View')  
 
    def insertprepay(self,**paras):       
        locator = queryUtility(IDbapi, name='onlinepay')
        locator.add(paras)
        return              
    
    def render(self):
        "response to front end"
        """def getSnsapiUserInfo(cls, access_token, openid, lang="zh_CN"):"""

        logger.info ("enter pay_ajax render.")
        datadic = self.request.form
        fee = float(datadic['fee'])        
        fee = round(fee,2)              
        total_fee = str(int(fee * 100))
        body = datadic['did']      
        openid = datadic['openid']       
        api = JsApi_pub()
        logger.info ("openid:%s,body:%s,total_fee:%s." % (openid,body,total_fee))
        out = api.getParameters(openid,body,total_fee)
        datadic['money'] = str(fee)
        datadic['status'] = 0
        datadic['openid'] = openid
        if datadic['aname'] =="":
            logger.info("start get nickname !")
            help_api = WeixinHelper()
            logger.info("authorize code is:%s" % datadic['code'])
            token = help_api.getAccessTokenByCode(datadic['code'])
            logger.info("access token is:%s" % token)
            userinfo = help_api.getSnsapiUserInfo(token,openid)
            logger.info("user nickname  is:%s" % userinfo['nickname'])            
            datadic['aname'] = userinfo['nickname']

        del datadic['fee']
        del datadic['code']
        self.insertprepay(**datadic)  
        self.request.response.setHeader('Content-Type', 'application/json')      
        return out        
            

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
                astr = i.atime.strftime('%Y-%m-%d')
                if astr == '2000-01-01':
                    atime = u""
                else:
                    atime = astr
                if bool(i.goods):
                    if bool(i.money):
                        money = "%s(%s)" % (i.money,i.goods)
                    else:
                        money = "(%s)" % (i.goods)
                else:
                    money = i.money
                out = """<tr class="text-left">
                                <td class="col-md-8">%(name)s</td>
                                <td class="col-md-1">%(money)s</td>
                                <td class="col-md-1">%(atime)s</td>
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
                                            money= money,
                                            atime= atime,
                                            edit_url="%s/@@update_donor/%s" % (contexturl,i.doid),
                                            delete_url="%s/@@delete_donor/%s" % (contexturl,i.doid))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                
                astr = i.atime.strftime('%Y-%m-%d')
                if astr == '2000-01-01':
                    atime = u""
                else:
                    atime = astr
                if bool(i.goods):
                    if bool(i.money):
                        money = "%s(%s)" % (i.money,i.goods)
                    else:
                        money = "(%s)" % (i.goods)
                else:
                    money = i.money                
                out = """<tr class="text-left">
                                <td class="col-md-10">%(name)s</td>
                                <td class="col-md-1">%(money)s</td>
                                <td class="col-md-1">%(atime)s</td>
                                </tr> """% dict(
                                            name=i.aname,
                                            money= money,
                                            atime= atime)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data

class SpecifyDonorajaxsearch(Donorajaxsearch):
    """AJAX action for search DB donor table.
    receive front end ajax transform parameters
    """

    grok.name('specify_donor_ajaxsearch')

    def searchview(self,viewname="specify_donor_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview


class GuangZhuangDonorajaxsearch(Donorajaxsearch):
    """AJAX action for search DB donor table.
    receive front end ajax transform parameters
    """

    grok.name('guanzhuang_donor_ajaxsearch')

    def searchview(self,viewname="guanzhuang_donor_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview


# Delete Update Input block
class DeleteDonate(form.Form):
    "delete the specify model recorder"
    implements(IPublishTraverse)
    grok.context(IJuanzenggongshi)
    grok.name('delete_donate')
    grok.require('xtcs.policy.input_db')

    label = _(u"delete donate data")
    fields = field.Fields(IDonate).omit('did','start_time')
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
      
        dtst = data['start_time']
        if isinstance(dtst,datetime):
            # datetime convert to timestamp
            dtst = time.strptime(dtst.strftime(fmt),fmt)
            dtst = int(time.mktime(dtst))
            
            data['start_time'] = dtst
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
    label = _(u"delete donate data")
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


class InputDonor(InputDonate):
    """input db donor table data
    """

    grok.name('input_donor')

    label = _(u"Input donor data")
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
        locator = getUtility(IDonateLocator)
        try:
            id = data['did']
            name = locator.getByCode(id).aname
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@donate_listings')                  

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        url_suffix = '/@@donor_listings?name=%s&id=%s' % (name,id)        
        self.request.response.redirect(self.context.absolute_url() + url_suffix)

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@donate_listings')


class UpdateDonor(UpdateDonate):
    """update model table row data
    """
    grok.name('update_donor')
    label = _(u"update donor data")
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
        data['id'] = self.id
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


