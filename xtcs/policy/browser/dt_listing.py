#-*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFPlone.resources import add_resource_on_request
from Products.CMFPlone.resources import add_bundle_on_request


class JuanZengView(BrowserView):
    """using datatable"""
    
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
        add_bundle_on_request(self.request, 'xtcs-policy-datatable')    