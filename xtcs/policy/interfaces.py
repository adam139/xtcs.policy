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
    """展示日常无固定指向项目的捐赠公示"""
class IYangguangwu (Interface):
    """展示已有捐赠的项目"""
    
class IJuanzengworkflow (Interface):
        """在线捐赠处理流程"""

class IContainerTablelist (Interface):
    """文件夹标记接口"""

# db insterface   
# db insterface
class IDbapi (Interface):
    """Db api """

    def __init__(session,package,table,factorycls,columns=None,fullsearch_clmns=None):
        """
        parameters:
        :session db mapper session,
        :package the package where table class in here. for example:'cms.db.orm',
        :table the database table name that will be query, 'admin_logs',
        :factorycls the class name that will be create table object instance,'AdminLog',
         or the class itself,AdminLog.
        :columns will be returned table columns,
        :fullsearch_clmns the columns that will been used keyword full text search
        """    
    
    def init_table():
        "import the table's mapper class named tablecls"
        
    def get_rownumber():
        "fetch table's rownumber"

    def bulk_delete():
        "bulk delete"
        
    def query(kwargs):
        """single table query 
        parameters:
        :kwargs's keys parameters:
            start:start location
            size:batch size
            keyword:full search keyword
            direction:sort direction
            max:batch size for Oracle
            with_entities:if using serial number fetch recorder's columns,1 True,0 False      
        """         
        
    def multi_query(kwargs,tmaper,tbl,tc,cv,key1,key2):
        """
        parameters:
        :kwargs's keys parameters:
            start:start location
            size:batch size
            keyword:full search keyword
            direction:sort direction
            max:batch size for Oracle
            with_entities:if using serial number fetch recorder's columns,1 True,0 False
        :tmaper: will joined table's mapper object
        :tbl: will joined table's name
        :tc:will be checked table column
        :cv:the tc should equal value
        :key1:first table primary key
        :key2:second table fk's refer to first table         
        """

    def update_asso_table(kwargs,searchcnd):
        """
        parameters:
        :kwargs:will be update data :type dict
        :searchcnd:the search condition that located the recorder, type: dict
        """    

    def search_clmns2sqltxt(self,clmns):
        """get columns that will been used keyword full text search
        :input:clmns = ['tit','des']
        :output:" tit LIKE :x OR des LIKE :x "                                  
        """

    def search_clmns4filter(clmns,tablecls,keyword):
        """get columns that will been used keyword full text search
        :input:clmns = ['tit','des']
        :input:tablecls = mapper object
        :input:keyword search keyword:string
        :output:" [getattr(tablecls, 'tit').like("%" + query + "%"),getattr(tablecls, 'des').like("%" + query + "%")] "
                                  
        """

    def pk_title(pk,factorycls,title):
        """primary key to row recorder 's title
        根据主键提取指定表对象的属性
        """

    def pk_obj_property(pk,rpt,title):
        """primary key to row recorder 's title
        根据主键查本表的关系属性,提取该关系属性指向的对象的指定属性
        parameters:
        pk:primary key:Long
        rpt:relative property:string
        title:target object's property:string
        """

    def pk_ass_title(pk,factorycls,asso,targetcls,fk,title):
        """通过主键查关联表,获取多对多的对象属性 
        #pk本地表主键  integer
        #factorycls 本地表类 cls
        #asso 关联表类  cls
        #targetcls 目标表类 cls 
        #fk关联表指向目标表外键名称 string
        #title目标表字段/属性    string
        """    

    def pk_ass_recorders(pk,factorycls,asso):
        """通过主键查关联表,获取多个关联表对象 
        #pk本地表主键  integer
        #factorycls 本地表类 cls
        #asso 关联表类  cls
        """    
 
    def pk_ass_obj_title(pk,factorycls,asso,targetcls,fk,title,mapf):
        """通过主键查关联表对象,获取多对多关联对象的属性 
        #pk本地表主键  integer
        #factorycls 本地表类 cls
        #asso 关联表类   cls
        #targetcls 目标表类  cls
        #fk关联表指向目标表外键名称 string
        #title目标表字段/属性    string
        #mapf 映射函数   function
        """

    def ex_pk_ass_obj_title(pk,factorycls,asso,asso_p1,asso_p2,midcls,midp,\
                            asso2,asso2_p1,asso2_p2,p2,fk,comp):
        """通过主键查关联表对象1,连接关联表2,获取多对多关联对象的属性 
        #pk本地表主键  integer
        #factorycls 本地表类 cls
        #asso 关联表1类   cls
        #asso_p1 关联表asso要提取的字段/属性    string
        #asso_p2 关联表asso要提取的字段/属性    string
        #p1目标表字段/属性    string                
        #midcls 中间表类
        #midp 中间表要提取的字段/属性    string
        #asso2 关联表2类  cls
        #asso2_p1 关联表asso2要提取的字段/属性    string
        #asso2_p2 关联表asso2要提取的字段/属性    string
        #p2关联表asso2字段/属性    string
        #fk关联表asso2对应p2的外键值 int
        #comp 两个关联表共有的主键字段/属性    string
        """
    
    def get_asso_obj(cns,cls=None):
        """query association object table 
        parameters:
        :cns:{'column1':'value1',...}
        :cls: will be queryed association table mapper object
        """
    
    
    def get_columns():
        "get all columns of single table"
        
    def join_columns(maper):
        "get two tables all columns when base table join the table that is provided by maper parameter"        
    
    def add(kwargs):
        "add single table recorder"
    
    def add_multi_tables(kwargs,fk_tables,asso_tables=[],asso_obj_tables=[]):
        """
        update all fk_tables,asso_tables and asso_obj_tables when add base table recorder
        fk_tables:[(pk,map_cls,attr),...]
        asso_tables:[([pk1,pk2,...],map_cls,attr),...]
        asso_obj_tables:{"asso_proxy_property1":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]),...],
                            "asso_proxy_property2":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]]
                            ,...}        
        """
    
    def update_multi_tables(kwargs,fk_tables=[],asso_tables=[],asso_obj_tables=[]):

        """
        update all fk_tables,asso_tables and asso_obj_tables when  update base table properties
        fk_tables:[(pk,map_cls,attr),...]
        asso_tables:[([pk1,pk2,...],map_cls,attr),...]
        asso_obj_tables:{"asso_proxy_property1":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]),...],
                            "asso_proxy_property2":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]]
                            ,...}
        """
        
    
    def fetch_oldest():
        "fetch the oldest recorder from db"
        
    def getByCode(id,pk=None):
        """get the recorder by table's primary key        
        parameters:
        id primary key's value: int
        pk primary field name: string
        """
        
    def DeleteByCode(id,pk=None):
        
        """delete the recorder
        parameters:
        id primary key' value: int
        pk primary field name: string
        """
        
    def deleteByKwargs(kwargs):
        "delete the first recorder where obey conditions that is provided by kwargs dictionary"
        
    def updateByCode(kwargs):
        """update the recorder by primary key that is provided by kwargs
        parameters:
        kwargs :dic
        here has two call case:
          1. kwargs should at least contain key 'id' that is default primary key,
        kwargs['id'] will as primary value for located the recorder.
          2. if kwargs also contain key 'pk',then primary key will be kwargs['pk'],
        and kwargs['id'] will as primary['pk'] 's value for located the recorder
        """
        
    def getByKwargs(**args):
        "get first recorder by multiple conditions that is provided by args dictionary"
        
    def getMultiByKwargs(**args):
         "get all recorders by multiple conditions that is provided by args dictionary"
        

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
       