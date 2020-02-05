#-*- coding: UTF-8 -*-
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from my315ok.wechat.interfaces import IwechatSettings
from my315ok.wechat.lib import WeixinHelper 

from xtcs.policy import _
from xtcs.policy.browser.interfaces import IThemeSpecific



oauth2url = 'https://open.weixin.qq.com/connect/oauth2/authorize'

class ZhiFuWeiXinAuthView(BrowserView):
        
    @memoize
    def outputjs2(self):
        "用户同意授权，获取code"
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        if bool(settings.appid):
            appid = settings.appid
        else:
            appid = "wx2833460b1571bd01"            
        if bool(settings.redirecturi):
            redirecturi = settings.redirecturi
        else:
            redirecturi = 'http://www.xtcs.org'
                          
        out = """
        function init() {
        var ruri = encodeURIComponent(%(ruri)s);
        var oauthUrl = '%(au2url)s?appid=%(appid)s&redirect_uri=' + ruri + '&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect';
        window.location.href = oauthUrl;
        }
        init();
        """ % dict(ruri=redirecturi,appid=appid,au2url=oauth2url)

        return out        

    @memoize
    def outputjs(self):
        "用户同意授权，获取code"
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        if bool(settings.appid):
            appid = settings.appid
        else:
            appid = "wx2833460b1571bd01"            
        if bool(settings.redirecturi):
            redirecturi = settings.redirecturi
        else:
            redirecturi = 'http://weixin.315ok.org/@@donated_workflow'
        nexturl = WeixinHelper.oauth2(redirecturi)
                          
        out = """
        function init() {
         window.location.href = "%(oauthUrl)s";
        }
        init();
        """ % dict(oauthUrl=nexturl)

        return out
    
class ZhiFuWeiXinPayView(BrowserView):
    "fetch access_token by code,"
    pass 
    
               
 