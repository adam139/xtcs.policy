#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope.component import getMultiAdapter
import json
from Products.Five.browser import BrowserView


class DtAjaxView(BrowserView):
    """receive datatable front end data,call db query,return result to dt front end"""
    
    def searchview(self,viewname="donor_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def __call__(self):
        searchview = self.searchview()
        # dt receive front end ajax post data
        dt = self.request.form
        draw = int(dt['draw'])
        start = int(dt['start'])
        size = int(dt['length'])
        keyword = dt['search[value]']
        order_by = dt['order[0][column]']
        direction = dt['order[0][dir]']
        id = int(dt['xiangmu_id'])
        total_col = dt['total_col']
        if direction == "desc":
            direction = "reverse"
        else:
            direction = "forward"

        origquery ={'start':start,'size':size,'with_entities':0,'SearchableText':keyword,'sort_order':direction}
        filterquery = {'status':1,'xiangmu_id':id}
        totalquery = origquery.copy()
        totalquery.update({'size':0,'SearchableText':''})
        keyquery = origquery.copy()
        keyquery.update({'size':0})
               
        recordsTotal = searchview.search_multicondition(totalquery,filterquery)
        recordsFiltered = searchview.search_multicondition(keyquery,filterquery)        
        origquery['order_by'] = 'juanzeng_shijian'
        resultDicLists = searchview.search_multicondition(origquery,filterquery)
        total = searchview.total_multicondition({'sumCol':total_col,'keyword':keyword},filterquery)
        data = []
        for i in resultDicLists:
            item = []
            item.append(i.xingming)
            item.append(float(i.xianjin))
            item.append(i.wuzi)
            item.append(i.juanzeng_shijian.strftime('%Y-%m-%d'))
            data.append(item)              
        
        result = {'draw':draw,'recordsTotal':recordsTotal,'recordsFiltered':recordsFiltered}
        result.update({'data':data,'xianjinTotal':float(total)})
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(result)              
        
