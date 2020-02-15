#-*- coding: UTF-8 -*-
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
from datetime import datetime,timedelta
from my315ok.wechat.lib import WeixinHelper
from xtcs.policy.mapping_db import  AccessToken
from xtcs.policy.interfaces import IDbapi
from zope.component import queryUtility 


class Base(BrowserView):
    """read request cookie"""
    
    def __init__(self,context, request):
        ""
        self.context = context
        self.request = request    
    
    def getOpenId(self):
        openid = self.request.cookies.get("openid", "")
        if bool(openid):
            locator = queryUtility(IDbapi, name='accesstoken')
            args = {"start":0,"size":1,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse','order_by':'id'}
            filter_args = {"openid":openid}
            rdrs = locator.query_with_filter(args,filter_args)
            if bool(rdrs) and rdrs[0].expiredtime  > datetime.now():
                return rdrs[0].openid
            else:
                return ""
        else:
            return ""            
        
    
    def __call__(self):
        ""
        openid = self.getOpenId()
        if bool(openid):
            url = "{0}?openid={1}".format(self.redirectUrl(),openid)
            self.request.response.redirect(url)
        else:
            self.request.response.redirect(self.winxinAuthUrl())
    
    def redirectUrl(self):
        return '{0}/@@pay'.format(self.context.absolute_url())
       
    
    def winxinAuthUrl(self):
        
        return WeixinHelper.oauth2(self.redirectUrl())

        
class HotBase(Base):
     
    def redirectUrl(self):
        return '{0}/@@hotpay'.format(self.context.absolute_url())
 
    
class ZhiFuWView(BrowserView):    
       
        
    @memoize
    def outputjs(self):
        "用户同意授权，获取code"
#         registry = getUtility(IRegistry)
#         settings = registry.forInterface(IwechatSettings)                          
        redirecturi = 'http://weixin.315ok.org/@@donated_workflow'
        nexturl = WeixinHelper.oauth2(redirecturi)
        out = """
        function init() {
         window.location.href = "%(oauthUrl)s";
        }
        init();
        """ % dict(oauthUrl=nexturl)
        return out
    
        
class ZhiFuWeiXinAuthView(ZhiFuWView):
    "fetch access_token by code,"

    @memoize
    def outputjs(self):
        "用户同意授权，获取code"
#         registry = getUtility(IRegistry)
#         settings = registry.forInterface(IwechatSettings)                          
        redirecturi = 'http://weixin.315ok.org/@@pay'
        nexturl = WeixinHelper.oauth2(redirecturi)
        out = """
        function init() {
         window.location.href = "%(oauthUrl)s";
        }
        init();
        """ % dict(oauthUrl=nexturl)
        return out


class ZhiFuHotAuthView(ZhiFuWView):
    "fetch access_token by code,"

    @memoize
    def outputjs(self):
        "用户同意授权，获取code"
#         registry = getUtility(IRegistry)
#         settings = registry.forInterface(IwechatSettings)                          
        redirecturi = 'http://weixin.315ok.org/@@currentpay'
        nexturl = WeixinHelper.oauth2(redirecturi)
        out = """
        function init() {
         window.location.href = "%(oauthUrl)s";
        }
        init();
        """ % dict(oauthUrl=nexturl)
        return out    
               
 