#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema

from xtcs.policy import _

class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

#文件夹mark interfaces,用于定义视图
# todo :定义db_ajax_listing view
class IAixinjuankuan (Interface):
    """某一捐赠项目具体捐赠记录"""
class IJuanzenggongshi (Interface):
    """展示已有捐赠的项目"""
class IJuanzengworkflow (Interface):
        """在线捐赠处理流程"""

class IContainerTablelist (Interface):
    """文件夹标记接口"""

# db insterface   

class IArticleLocator (Interface):
    """Article table add row"""

    def add(**kwargs):
        "add a row data"

    def query(code):
        "query  by search condition"

    def getByCode(code):
        "query  by search condition"
        
    def deleteByCode(code):
        "query  by search condition"        

    def updateByCode(code):
        "query  by search condition"
class IProjectLocator (IArticleLocator):
    """Project table add row """
class IDonorLocator (IArticleLocator):
    """donor table add row donor"""
class IVolunteerteamLocator (IArticleLocator):
    """Volunteerteam table add row donor """    
class IDonateLocator (IArticleLocator):
    """donate table add row donor """
       