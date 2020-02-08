#-*- coding: UTF-8 -*-
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
# from zope.component import getUtility
# from plone.registry.interfaces import IRegistry
# from my315ok.wechat.interfaces import IwechatSettings
from my315ok.wechat.lib import WeixinHelper 


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
    
               
 