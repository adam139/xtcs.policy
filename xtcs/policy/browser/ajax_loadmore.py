#-*- coding: UTF-8 -*-
from five import grok
import json
from Acquisition import aq_inner
from zope.interface import Interface
from zope.component import getMultiAdapter
from Products.CMFCore import permissions
from plone.app.contenttypes.permissions import AddDocument
from Products.CMFCore.utils import getToolByName
from plone.app.contenttypes.interfaces import IFolder,IFile,IDocument,ILink
from Products.Five.utilities.marker import mark
from Products.CMFCore.interfaces import ISiteRoot
from plone.memoize.instance import memoize
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity.utils import createContentInContainer
from xtcs.policy.browser.interfaces import IThemeSpecific
from Products.Five.browser import BrowserView
import datetime    


class ContainerTableListView(BrowserView):

#     grok.layer(IThemeSpecific)  
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc    
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
      
        return self.pm().checkPermission(permissions.ManagePortal,self.context)
    
    @property
    def isAddable(self):

        return self.pm().checkPermission(permissions.AddPortalContent,self.context)  
        
    def getFolders(self):
        """获取当前目录所有文件夹对象"""       

        braindata = self.catalog()({'object_provides':IFolder.__identifier__,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
 
    def objmarks(self):
        objmarks = [IFile.__identifier__,
                    IDocument.__identifier__,
                    ILink.__identifier__
                    ]
        return objmarks
        
    def allitems(self):
        objmarks = self.objmarks()
        try:
            from my315ok.products.product import Iproduct
            objmarks.append(Iproduct.__identifier__)
            braindata = self.catalog()({'object_provides':objmarks,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              ) 
        except:            
            braindata = self.catalog()({'object_provides':objmarks,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              ) 

        return braindata         
        
    def getDocuments(self,start,size):
        """获取所有页面"""

        if size ==0:return self.allitems()
        objmarks = self.objmarks()
        try:
            from my315ok.products.product import Iproduct
            objmarks.append(Iproduct.__identifier__)
            braindata = self.catalog()({'object_provides':objmarks,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'b_start':start,
                             'b_size':size}                              
                                              ) 
        except:
            
            braindata = self.catalog()({'object_provides':objmarks,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'b_start':start,
                             'b_size':size}                               
                                              ) 

        return braindata 

    
    def pendingDefault(self):
        "计算缺省情况下，还剩多少条"
        total = len(self.allitems())
        if total > 10:
            return total -10
        else:
            return 0
        
    @memoize
    def getTableList(self,start,size):
        """获取行政许可列表"""

        braindata = self.getDocuments(start,size)
        return self.outhtmlList(braindata)
             
    def outhtmlList(self,braindata):
        outhtml = ""
        
        for i in braindata:            
            out = """<tr>
            <td class="col-md-9 title"><a href="%(url)s">%(title)s</a></td>
            <td class="col-md-3 item">%(pubtime)s</td>
            </tr>""" % dict(url = i.getURL(),
                            title = i.Title,
                            pubtime = i.created.strftime('%Y-%m-%d'))           
            outhtml = "%s%s" %(outhtml ,out)
        return outhtml 
class favoritemore(grok.View):
    """AJAX action for container table click more.
    """
    
    grok.context(IFolder)
    grok.name('favoritemore')
    grok.require('zope2.View')            
    
    def render(self):
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst)*10 
        nextstart = formstart + 10                
        favorite_view = getMultiAdapter((self.context, self.request),name=u"tableview")
        favoritenum = len(favorite_view.allitems())
        
        if nextstart >= favoritenum :
            ifmore =  1
            pending = 0
        else :
            ifmore = 0  
            pending = favoritenum - nextstart          
        braindata = favorite_view.getDocuments(formstart,10)        
        outhtml = ""

        pending = "%s" % (pending)
        for i in braindata:
          
            out = """<tr>
            <td class="col-md-9 title"><a href="%(url)s">%(title)s</a></td>
            <td class="col-md-3 item">%(pubtime)s</td>
            </tr>""" % dict(url = i.getURL(),
                            title = i.Title,
                            pubtime = i.created.strftime('%Y-%m-%d'))           
            outhtml = "%s%s" %(outhtml ,out)
            
        data = {'outhtml': outhtml,'pending':pending,'ifmore':ifmore}
    
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)

