#-*- coding: UTF-8 -*-
from __future__ import division
from plone import api
from zope.interface import Interface
from zope.component import getMultiAdapter
import json
import urllib
from datetime import datetime
from datetime import timedelta
from plone.registry.interfaces import IRegistry
from xtcs.policy.browser.interfaces import IwechatSettings
from xtcs.policy import fmt
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from plone.app.contenttypes.permissions import AddDocument
from plone.memoize.instance import memoize
from xtcs.policy import _
from Products.Five.browser import BrowserView
from zope.component import getUtility,queryUtility
from plone.directives import form
from z3c.form import field, button
from Products.statusmessages.interfaces import IStatusMessage
from xtcs.policy.interfaces import InputError
from sqlalchemy.dbapi.interfaces import IDbapi
from xtcs.policy.mapping_db import IXiangMu,IJuanZeng
from xtcs.policy.mapping_db import JuanZeng
from my315ok.wechat.pay import WeixinHelper
from my315ok.wechat.pay import UnifiedOrder_pub
from my315ok.wechat.pay import JsApi_pub
from my315ok.wechat.pay import Wxpay_server_pub
from my315ok.wechat.pay import OrderQuery_pub
from my315ok.wechat.pay import WxPayConf_pub
from my315ok.wechat.lib import HttpClient 
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.CMFPlone.resources import add_bundle_on_request
from zExceptions import NotFound
from xtcs.policy.utility import fetch_url_parameters
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
#         logger.info("enter get accesstoken")
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        stime = settings.access_token_time
        token = settings.access_token
#         logger.info("old token is:%s,old time is:%s" % (token,stime))
        if bool(token) and stime + timedelta(seconds=7000) > datetime.now():
            return token        
#         _ACCESS_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
#         token = HttpClient().get(_ACCESS_URL.format(WxPayConf_pub.APPID, WxPayConf_pub.APPSECRET))
        token = super(CustomWeixinHelper,cls).getAccessToken()
#         logger.info("new token is:%s" % token)
        import ast
        token = ast.literal_eval(token)
        if 'errcode' not in token.keys(): 
#             logger.info("new token '%s' saved to cache" % token['access_token'])
            settings.access_token_time = datetime.now()
            settings.access_token = token['access_token']
        return token['access_token']


    @classmethod
    def getAccessTokenByCode(cls, code):
        """通过code换取网页授权access_token, 该access_token与getAccessToken()返回是不一样的
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """

        logger.info("enter getAccessTokenByCode. code:'%s'" % code)        
        token =  super(CustomWeixinHelper,cls).getAccessTokenByCode(code)
        import ast
        if isinstance(token,str):            
            token = ast.literal_eval(token)        
        if 'errcode' not in token.keys():
            #refresh access_token
            token = super(CustomWeixinHelper,cls).refreshAccessToken(token['refresh_token'])
            logger.info("new refresh token is:%s" % token)
            if isinstance(token,str):                
                token = ast.literal_eval(token)
            if 'errcode' not in token.keys():
                #new openid accesstoken expire_time write to db
                locator = queryUtility(IDbapi, name='accesstoken')
                timelimit = datetime.now + timedelta(seconds=token['expires_in'])
                openid = token['openid']
                data = {"openid":openid,"token":token['access_token'],
                            "expiredtime":timelimit}
                query_args = {"start":0,"size":1,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}
                filter_args = {"openid":openid}
                rdrs = locator.query_with_filter(query_args,filter_args)
                if bool(rdrs):
                    data['id'] = rdrs[0].id
                    locator.updateByCode(data)
                else:
                    #new user
                    locator.add(data)
                return token
            else:
                return {}
        else:
            return {}


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
        ticket = super(CustomWeixinHelper,cls).getJsapiTicket(access_token)
        settings.jsapi_ticket_time = datetime.now()
        settings.jsapi_ticket = ticket         
        return ticket    


class TokenAjax(BrowserView):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def getAccessTokenByCode(self):        
        try:
            code = self.request.form['code']      
            return WeixinHelper.getAccessTokenByCode(code)
        except:
            return ""

    def updateToken(self,token):
        if 'errcode' not in token.keys():        
            locator = queryUtility(IDbapi, name='accesstoken')
            timelimit = datetime.now() + timedelta(seconds=token['expires_in'])
            openid = token['openid']
            data = {"openid":openid,"token":token['access_token'],
                            "expiredtime":timelimit}
            query_args = {"start":0,"size":1,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}
            filter_args = {"openid":openid}
            rdrs = locator.query_with_filter(query_args,filter_args)
            if bool(rdrs):
                data['id'] = rdrs[0].id
                locator.updateByCode(data)
            else:                   
                locator.add(data)
            self.request.response.setCookie("openid", token["openid"])        
        
    
    def __call__(self):
        "response to front end"       
    
        token = self.getAccessTokenByCode()
        #set cookie for store openid
        import ast
        if isinstance(token,str):
            token2 = ast.literal_eval(token)
        self.updateToken(token2)
        self.request.response.setHeader('Content-Type', 'application/json')
        return token                   


class NotifyAjax(object):    
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def __call__(self):
        """weixin callback"""        
#         logger.info("weixin callback ------entering !")
        self.request.response.setHeader('Content-Type', 'text/plain')
        if self.request['method'] == 'GET':
#             logger.info("received get quest=get !")
            self.request.response.setHeader('Content-Type', 'application/xml')          
            return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"

        if "xml" not in self.request:return "no"     
        datadic = self.request['xml']        
#         logger.info(str(datadic))   
        datadic = WeixinHelper.xmlToArray(datadic)
        if 'result_code' not in datadic:
            return "no"
        elif datadic['result_code'] == "FAIL":
            return "no"
        base = Wxpay_server_pub()
        openid = datadic['openid']
        money =  datadic['total_fee']        
        money = int(money)/100  
        base.data = datadic
        locator = queryUtility(IDbapi, name='juanzeng')
#         验证签名和金额是否一致 金额在用户下单插入数据库
        query_data = {"start":0,"size":1,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}
        filter_args = {"openid":openid,"xianjin":float(money)}
        recorders = locator.query_with_filter(query_data,filter_args)
#         recorder = Session.query(JuanZeng).filter(JuanZeng.openid==openid).\
#             filter(JuanZeng.xianjin==float(money)).\
#             order_by(JuanZeng.id.desc()).first()
        if not bool(recorders):return "no"
        recorder = recorders[0]
        if bool(recorder.status):return "no"        
        if base.checkSign():            
            # update status=1
            locator.updateByCode({"id":recorder.id,"status":1})
            # send template message
            try:
                message = u"湘潭市慈善总会于:{0},收到您的捐款:{1}元,感谢您的善心善行!"
                nw = datetime.now().strftime(fmt)
                text = message.format(nw,money).encode('utf-8')
#                 logger.info("start send text message:%s" % text)
                access_token = CustomWeixinHelper.getAccessToken()
#                 logger.info("base accesstoken:%s" % access_token)
                WeixinHelper.sendTextMessage(openid, text, access_token)
            except:
                logger.info("send text message:'%s'failed"  % text)
            return 'ok'                    
        else:            
            return 'no'             


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
 

class PayAjax(BrowserView):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
 
    def insertprepay(self,**paras):       
        locator = queryUtility(IDbapi, name='juanzeng')
        locator.add(paras)
        return              
    
    def __call__(self):
        "response to front end"
        """def getSnsapiUserInfo(cls, access_token, openid, lang="zh_CN"):"""

        datadic = self.request.form
        fee = float(datadic['fee'])        
        fee = round(fee,2)              
        total_fee = str(int(fee * 100))
        id = datadic['did']      
        openid = datadic['openid']
        locator = queryUtility(IDbapi, name='xiangmu')
        xrdr = locator.getByCode(id)
        body = xrdr.mingcheng.encode('utf-8')     
        out = JsApi_pub().getParameters(openid,body,total_fee)
        rdr = {}
#         datadic['money'] = str(fee)
        rdr['xiangmu_id'] = xrdr.id
        rdr['xianjin'] = float(fee)
        rdr['status'] = 0
        rdr['openid'] = openid
        if datadic['aname'] =="":
            try:
                logger.info("start get nickname !")
                locator = queryUtility(IDbapi, name='accesstoken')
                query_args = {"start":0,"size":1,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}
                filter_args = {"openid":openid}
                rdrs = locator.query_with_filter(query_args,filter_args)
                token = rdrs[0].token
                userinfo = WeixinHelper.getSnsapiUserInfo(token,openid)
                logger.info("user nickname  is:%s" % userinfo['nickname'])            
                datadic['aname'] = userinfo['nickname']
            except:
                logger.info("fetch  nickname failed !")
                datadic['aname'] == u"匿名".encode('utf-8')                

#         del datadic['fee']
        rdr['xingming'] = datadic['aname']
        rdr['juanzeng_shijian'] = datetime.now()
        self.insertprepay(**rdr)  
        self.request.response.setHeader('Content-Type', 'application/json')      
        return out        
            

class WeixinPay(BrowserView):
    """
    在线捐款流程。
    view name:donated_workflow
    """
    def getProjectId(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        if bool(settings.hot_project):        
            return settings.hot_project
        else:
            return 6 
        
    def get_projects(self,id=None):
        "提取系统所有公益项目"

        query_args = {"start":0,"size":20,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}      
        locator = queryUtility(IDbapi, name='xiangmu')
        recorders = locator.query(query_args)

        def outfmt(rcd):
            out = '<label><input type="radio" name="{0}" id="{1}" value="{2}">{3}</label>'
            name = "project{0}".format(rcd.id)
            out = out.format("project",name,rcd.id,rcd.mingcheng)
            return out
            
        outhtml = map(outfmt,recorders)
        if bool(outhtml):
            first = outhtml[0]
            index = first.find('value') 
            outhtml[0] = first[:index] + ' checked ' + first[index:]
             
        outhtml = "<p></p>".join(outhtml)
        return outhtml

class CurrentWeixinPay(WeixinPay):
    """
    在线捐款流程。
    view name:donated_workflow
    """       
        
    def get_projects(self,id=None):
        "提取当前公益项目,id is project id"
        if id==None:
            id = self.getProjectId()
        locator = queryUtility(IDbapi, name='xiangmu')
        rcd = locator.getByCode(id)
        out = dict()
        out['title'] = rcd.mingcheng
        st = '<label><input type="radio" name="{0}" id="{1}" value="{2}" checked>{3}</label>'
        pid = "project{0}".format(rcd.id)
        out['html']  = st.format("project",pid ,rcd.id,rcd.mingcheng)
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
            
    def getHotProject(self):
        id = self.getProjectId()
        locator = queryUtility(IDbapi, name='xiangmu')
        rcd = locator.getByCode(id)
        out = "<h1>%s</h1><p>%s<p>" % (rcd.mingcheng,rcd.jieshao)
        return out        

    def get_projects(self):
        "提取系统所有公益项目"

        query_args = {"start":0,"size":10,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}      
        locator = queryUtility(IDbapi, name='xiangmu')
        filter_args = {"youxiao":1}               
        recorders = locator.query_with_filter(query_args,filter_args)        

        def outfmt(rcd):
            out = '<li>{0}</li>'.format(rcd.mingcheng)
            return out
            
        outhtml = map(outfmt,recorders)             
        outhtml = '<ul class="available">{0}</ul>'.format("".join(outhtml))
        return outhtml

    @memoize
    def outputjs(self):
        ""                         
        portal_url = api.portal.get().absolute_url()
        hoturl = "{0}/@@hotauth".format(portal_url)
        selectutl = "{0}/@@auth".format(portal_url)
        
        out = """
$(document).ready(function(){        
    $(".hot-project").on("click",function (e) {
          e.preventDefault();
          window.location.href = "%(hoturl)s";
        });
    $(".self-select").on("click",function (e) {
          e.preventDefault();
          window.location.href = "%(selectutl)s";
        });
    });
        """ % dict(hoturl=hoturl,selectutl=selectutl)
        return out

class DonortableView(BrowserView):
    "捐赠金榜,显示日常捐赠"
      
    @memoize
    def getMemberList(self,start=0,size=0):
        """获取捐赠结果列表"""
        
        locator = queryUtility(IDbapi, name='juanzeng')
        query_args = {"start":0,"size":1000,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}
        filter_args = {"xiangmu_id":5}               
        articles = locator.query_with_filter(query_args,filter_args)
        if articles == None:
            return             
        return self.outputList(articles)

    def outputList(self,braindata): 
        outhtml = ""
       
        for i in braindata:
            astr = i.juanzeng_shijian.strftime('%Y-%m-%d')
            if astr != '2000-01-01':
                atime = astr
            else:
                atime= u""                        
            if bool(i.wuzi):
                if bool(i.xianjin):
                    money = "%s(%s)" % (float(i.xianjin),i.wuzi)
                else:
                    money = "(%s)" % (i.wuzi)
            else:
                money = float(i.xianjin)            
            out = """<tr>
            <td class="title">%(title)s</td>
            <td class="item">%(money)s</td>
            <td class="atime">%(atime)s</td></tr>""" % dict(
                                            title=i.xingming,
                                            money= money,
                                            atime=atime)           
            outhtml = "%s%s" %(outhtml ,out)
        return outhtml

class GuanZhuangDonortableView(DonortableView):
    "冠状疫情捐赠"
      
    @memoize
    def getMemberList(self,start=0,size=0):
        """获取捐赠结果列表"""
        
        locator = queryUtility(IDbapi, name='juanzeng')
        data = {"start":0,"size":1000,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}
        filter_args = {"xiangmu_id":6}               
        articles = locator.query_with_filter(data,filter_args)
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
        locator = queryUtility(IDbapi, name='xiangmu')
     
        recorders = locator.query(query)
        return recorders

# donor table
class DonorView(DonateView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_ajax_juanzeng
    """

    def search_multicondition(self,query_args,filter_args):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = queryUtility(IDbapi, name='juanzeng')
        recorders = locator.query_with_filter(query_args,filter_args)
        return recorders
    
    def total_multicondition(self,query_args,filter_args):
        "query is dic,like :{'sumCol':'id','keyword':'key'}"
        
        locator = queryUtility(IDbapi, name='juanzeng')
        recorders = locator.total_query_with_filter(query_args,filter_args)
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
     

 # ajax multi-condition search relation db
class AjaxSearch(BrowserView):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
    
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

    def __call__(self):
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = self.searchview()
 # datadic receive front ajax post data
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        size = int(datadic['size'])      # batch search size
#         sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = datadic['searchabletext'].strip()
        origquery = {}
#         origquery['order_by'] = sortcolumn
        # sql db sortt_order:asc,desc
        origquery['sort_order'] = sortdirection
#  #模糊搜索

        origquery['SearchableText'] = keyword
#origquery provide  batch search
        origquery['size'] = size
        origquery['start'] = start
#         origquery['id'] = id
        origquery['with_entities'] = 0
#totalquery  search all
        totalquery = origquery.copy()
        totalquery['size'] = 0
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
                regtime = i.zhuceshijian            
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
                                </tr> """% dict(objurl="%s/@@donor_listings?name=%s&id=%s" % (contexturl,i.mingcheng,i.id),
                                                name = "%s" %  urllib.quote_plus(i.mingcheng.encode('utf-8')),                                                
                                                id = "%s" % i.id,
                                                num=str(k + 1),
                                                regtime = regtime.strftime("%Y-%m-%d"),
                                                title=i.mingcheng,
                                                edit_url="%s/@@update_donate/%s" % (contexturl,i.id),
                                                delete_url="%s/@@delete_donate/%s" % (contexturl,i.id))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                regtime = i.zhuceshijian         
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-9 text-left">
                                <a class="donate" data-name="%(name)s" data-id="%(id)s" href="%(objurl)s">%(title)s</a>
                                </td>
                                <td class="col-md-2">%(regtime)s</td>
                                </tr> """% dict(objurl="%s/@@juanzeng_listings_dt?name=%s&id=%s" % (contexturl,i.mingcheng,i.id),
                                                name = "%s" %  urllib.quote_plus(i.mingcheng.encode('utf-8')),                                                 
                                                id = "%s" % i.id,
                                                num=str(k + 1),
                                                regtime = regtime.strftime("%Y-%m-%d"),
                                                title=i.mingcheng)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data




class Donorajaxsearch(AjaxSearch):
    """AJAX action for search DB donor table.
    receive front end ajax transform parameters
    """


    def searchview(self,viewname="donor_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def __call__(self):
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = self.searchview()
 # datadic receive front ajax post data
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        size = int(datadic['size'])      # batch search size
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = datadic['searchabletext'].strip()
        id = int(datadic['id'])
        origquery = {}
        origquery['order_by'] = sortcolumn
        # sql db sortt_order:asc,desc
        origquery['sort_order'] = sortdirection
#  #模糊搜索       
        origquery['SearchableText'] = keyword
#origquery provide  batch search
        origquery['size'] = size
        origquery['start'] = start
#         origquery['id'] = id
        origquery['with_entities'] = 0
        filterquery = {'xiangmu_id':id}
        locator = queryUtility(IDbapi, name='xiangmu')
        name = locator.getByCode(id).mingcheng        
#totalquery  search all
        totalquery = origquery.copy()
        totalquery['size'] = 0
        # search all   size = 0 return numbers of recorders
        totalnum = searchview.search_multicondition(totalquery,filterquery)
        resultDicLists = searchview.search_multicondition(origquery,filterquery)
        del origquery
        del totalquery
        data = self.output(start,size,id,name,totalnum, resultDicLists)              
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
    
    def output(self,start,size,id,name,totalnum,resultDicLists):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if bool(self.searchview().isAddable):        
            for i in resultDicLists:
                astr = i.juanzeng_shijian.strftime('%Y-%m-%d')
                if astr == '2000-01-01':
                    atime = u""
                else:
                    atime = astr
                if bool(i.wuzi):
                    if bool(i.xianjin):
                        money = "%s(%s)" % (float(i.xianjin),i.wuzi)
                    else:
                        money = "(%s)" % (i.wuzi)
                else:
                    money = float(i.xianjin)

                url_suffix = "{0}?name={1}&id={2}".format(i.id,name,id)
                out = """<tr class="text-left">
                                <td class="col-md-5">%(name)s</td>
                                <td class="col-md-4">%(money)s</td>
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
                                </tr> """ % dict(
                                    name=i.xingming,
                                    money= money,
                                    atime= atime,
                                    edit_url="%s/@@update_donor/%s" % (contexturl,url_suffix),
                                    delete_url="%s/@@delete_donor/%s" % (contexturl,url_suffix))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                
                astr = i.juanzeng_shijian.strftime('%Y-%m-%d')
                if astr == '2000-01-01':
                    atime = u""
                else:
                    atime = astr
                if bool(i.wuzi):
                    if bool(i.xianjin):
                        money = "%s(%s)" % (float(i.xianjin),i.wuzi)
                    else:
                        money = "(%s)" % (i.wuzi)
                else:
                    money = float(i.xianjin)                
                out = """<tr class="text-left">
                                <td class="col-md-7">%(name)s</td>
                                <td class="col-md-4">%(money)s</td>
                                <td class="col-md-1">%(atime)s</td>
                                </tr> """% dict(
                                            name=i.xingming,
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

    def searchview(self,viewname="specify_donor_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview


class GuangZhuangDonorajaxsearch(Donorajaxsearch):
    """AJAX action for search DB donor table.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="guanzhuang_donor_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

# Delete Update Input block
class DeleteDonate(form.Form):
    "delete the specify model recorder"
    implements(IPublishTraverse)

    label = _(u"delete donate data")
    fields = field.Fields(IXiangMu).omit('id')
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
        locator = queryUtility(IDbapi, name='xiangmu')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        super(DeleteDonate, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete model recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='xiangmu')
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

    label = _(u"Input donate data")
    fields = field.Fields(IXiangMu).omit('id')
    ignoreContext = True

    def update(self):
        self.request.set('disable_border', True)
        super(InputDonate, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit donate recorder
        """
        data, errors = self.extractData() 
        if errors:
            self.status = self.formErrorsMessage
            return

        funcations = queryUtility(IDbapi, name='xiangmu')
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

    label = _(u"update donate data")
    fields = field.Fields(IXiangMu).omit('id')
    ignoreContext = False
    id = None
    # reset content
    def getContent(self):
        locator = queryUtility(IDbapi, name='xiangmu')
        return locator.getByCode(self.id)

    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()

    def update(self):
        self.request.set('disable_border', True)
        super(UpdateDonate, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='xiangmu')
        data['id'] = self.id
#         data['pk'] = "did"
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

class DeleteDonor(DeleteDonate):
    "delete the specify donor recorder"

    label = _(u"delete donate data")
    fields = field.Fields(IJuanZeng).omit('id')

    id = None
    #receive url parameters    
    def redirectUrl(self):
        pars = self.request['HTTP_REFERER'].split('?')
        if len(pars) > 1:
            urlpars = pars[1]
            result = fetch_url_parameters(urlpars)
            if result.has_key('name') and result.has_key('id'): 
                rdurl = "/@@donor_listings/?name={0}&id={1}".format(result['name'],result['id'])
            else:
                rdurl = "/@@donate_listings"
        else:
            rdurl = "/@@donate_listings"
        return rdurl
        
    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name              
            return self
        else:
            raise NotFound()

    def getContent(self):
        locator = queryUtility(IDbapi, name='juanzeng')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        super(DeleteDonor, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete model recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='juanzeng')
        rdurl = self.redirectUrl()
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + rdurl)
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + rdurl)

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        rdurl = self.redirectUrl()
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + rdurl)


class InputDonor(InputDonate):
    """input db donor table data
    """

    label = _(u"Input donor data")
    fields = field.Fields(IJuanZeng).omit('id','openid')

    def update(self):
        self.request.set('disable_border', True)
        super(InputDonor, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit model recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='juanzeng')
        locator = queryUtility(IDbapi, name='xiangmu')
        try:
            id = data['xiangmu_id']
            name = locator.getByCode(id).mingcheng
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


class UpdateDonor(DeleteDonor):
    """update model table row data
    """

    label = _(u"update donor data")
    fields = field.Fields(IJuanZeng).omit('id','xiangmu_id','openid')
    id = None              
    
    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name              
            return self
        else:
            raise NotFound()

    def getContent(self):                                         
        locator = queryUtility(IDbapi, name='juanzeng')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
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
        # add self define primary key parameter
#         data['pk'] = "doid" 
        funcations = queryUtility(IDbapi, name='juanzeng')        
        rdurl = self.redirectUrl()
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + rdurl)
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + rdurl)

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        rdurl = self.redirectUrl()
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + rdurl)
