#-*- coding: UTF-8 -*-
import sys
from datetime import datetime
from zope import schema


from zope import event
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import or_
from xtcs.policy import Scope_session as session
from xtcs.policy.interfaces import IDbapi
import datetime
from xtcs.policy import fmt
from xtcs.policy import linkstr
from xtcs.policy import _

class Dbapi(object):
    """Sqlalchemy ORM  db API base class"""
    
    implements(IDbapi)
    
    def __init__(self,session,package,table,factorycls,columns=None,fullsearch_clmns=None):
        """
        parameters:
        :session db mapper session,
        :package the package where table class in here. for example:'xtcs.policy.mapping_db',
        :table the table name that will be query, 'admin_logs',
        :factorycls the class name that will be create table object instance,'AdminLog',
         or the class itself,AdminLog.
        :columns will return table columns,
        :fullsearch_clmns the columns that will been used keyword full text search
        """
        
        self.session = session
        self.package = package
        self.table = table
        self.factorycls = factorycls
        self.columns = columns
        self.fullsearch_clmns = fullsearch_clmns        
        import os
        os.environ['NLS_LANG'] = '.AL32UTF8'      

    def search_clmns2sqltxt(self,clmns):
        """get columns that will been used keyword full text search
        :input:clmns = ['tit','des']
        :output:" tit LIKE :x OR des LIKE :x "
                                  
        """
        if self.fullsearch_clmns == None:
            return ""                       
        else:
            srts =[]
            for i in clmns:
                srt = "%(c)s LIKE :x" % dict(c=i)
                srts.append(srt)
            out = " OR ".join(srts)
            return out        

    def search_clmns4filter(self,clmns,tablecls,keyword):
        """get columns that will been used keyword full text search
        :input:clmns = ['tit','des']
        :output:" [getattr(tablecls, 'tit').like("%" + query + "%"),getattr(tablecls, 'des').like("%" + query + "%")] "
                                  
        """
        if self.fullsearch_clmns == None:
            return ""                       
        else:
            out = map(lambda x:getattr(tablecls, x).like("%" + keyword + "%"),self.fullsearch_clmns)
            return out        
        
    def pk_title(self,pk,factorycls,title):
        "primary key to row recorder 's title"
        "根据主键提取指定表对象的属性"
       
        recorder = session.query(factorycls).filter(factorycls.id==pk).one()
        return getattr(recorder,title,"")

    def pk_obj_property(self,pk,rpt,title):
        """primary key to row recorder 's title
        根据主键查本表的关系属性,提取该关系属性指向的对象的指定属性
        parameters:
        pk:primary key:Long
        rpt:relative property:string
        title:target object's property:string
        """
       
        tablecls = self.init_table()
        recorder = session.query(tablecls).filter(tablecls.id==pk).one()
        robj = getattr(recorder,rpt,"")
        return getattr(robj,title,"")

    def pk_ass_recorders(self,pk,factorycls,asso):
        "通过主键查关联表,获取多个关联表对象 "
        #pk本地表主键  integer
        #factorycls 本地表类 cls
        #asso 关联表类  cls     
 
        recorders = session.query(asso).join(factorycls).filter(factorycls.id==pk).all()
        return recorders

    def pk_ass_title(self,pk,factorycls,asso,targetcls,fk,title):
        "通过主键查关联表,获取多对多的对象属性 "
        #pk本地表主键  integer
        #factorycls 本地表类 cls
        #asso 关联表类  cls
        #targetcls 目标表类 cls 
        #fk关联表指向目标表外键名称 string
        #title目标表字段/属性    string       
 
        recorders = session.query(asso).join(factorycls).filter(factorycls.id==pk).all()
#       recorders:  [(37L, 109L)]
        def mapf(recorder):
            fkv = set(list(recorder))
            if len(fkv) > 1:fkv.remove(pk)
            target = session.query(targetcls).filter(targetcls.id ==list(fkv)[0]).one()
            return getattr(target,title,"")
        more = map(mapf,recorders)
        out = ",".join(more)
        return out
            
    def pk_ass_obj_title(self,pk,factorycls,asso,targetcls,fk,title,mapf):
        "通过主键查关联表对象,获取多对多关联对象的属性 "
        #pk本地表主键  integer
        #factorycls 本地表类 cls
        #asso 关联表类   cls
        #targetcls 目标表类  cls
        #fk关联表指向目标表外键名称 string
        #title目标表字段/属性    string
        #mapf 映射函数  function       
    
        recorders = session.query(asso).join(factorycls).filter(factorycls.id==pk).all()
        more = map(mapf,recorders)
        out = ";".join(more)
        return out

    def ex_pk_ass_obj_title(self,pk,factorycls,asso,asso_p1,asso_p2,midcls,midp,\
                            asso2,asso2_p1,asso2_p2,p2,fk,comp):
        "通过主键查关联表对象1,连接关联表2,获取多对多关联对象的属性 "
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
              
   
        stmt2 = session.query(asso2).filter(getattr(asso2,p2)==fk).subquery()
        stmt = session.query(asso).join(factorycls).filter(factorycls.id==pk).subquery()
        #[(u'\u767d\u828d', 7L, u'\u6652\u5e72', 0.26, 700L), (u'\u6842\u679d', 10L, u'\u63b0\u5f00', 0.36, 800L)]        
        recorders = session.query(getattr(midcls,midp),getattr(stmt.c,asso_p1),getattr(stmt.c,asso_p2),
                                   getattr(stmt2.c,asso2_p1),getattr(stmt2.c,asso2_p2)).\
        join(stmt,midcls.id ==getattr(stmt.c,comp)).join(stmt2,getattr(stmt2.c,comp)==getattr(stmt.c,comp)).all()
        return recorders


    def get_asso_obj(self,cns,cls=None):
        "query association object table "
        "cns:{'column1':'value1',...}"
        
        if bool(cls):
            tablecls = cls
        else:
            tablecls = self.init_table()
        conds = [] 
        for i in cns.keys():
            cn = "%s=%s" % (i,cns[i])
            conds.append(cn)
        conds = " AND ".join(conds)
        rt = self.session.query(tablecls).filter(text(conds)).first()
        return rt                          
        
    def get_columns(self):
        "get return columns by query"
        
        if self.columns == None:
            tablecls = self.init_table()
            from sqlalchemy.inspection import inspect
            table = inspect(tablecls)
            columns = [column.name for column in table.c]
            return columns                        
        else:
            return self.columns            

    def join_columns(self,maper):
        "return them' columns when join two tables "
        
        if self.columns == None:
            tablecls = self.init_table()
            from sqlalchemy.inspection import inspect
            table = inspect(tablecls)
            table2 = inspect(maper)
            columns = [column.name for column in table.c]
            column2 = [column.name for column in table2.c]
            return columns + column2                       
        else:
            return self.columns
            
    def add(self,kwargs):
        
        tablecls = self.init_table()
        recorder = tablecls()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        try:
            session.commit()
#             self.fire_event(RecorderCreated,recorder)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def add_multi_tables(self,kwargs,fk_tables,asso_tables=[],asso_obj_tables=[]):
        "添加表记录的同时,并关联其他表记录"
        # 外键关联表 fk_tables: [(pk,map_cls,attr),...]
        # 多对多关联表 asso_tables:[([pk1,pk2,...],map_cls,attr),...]
        # 多对多关联表(asso table has itself properties) 
        # asso_obj_tables:[(pk,targetcls,attr,[property1,property2,...]),...]
        tablecls = self.init_table() 
        recorder = tablecls()

        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        for i in fk_tables:
            mapcls = i[1]
            linkobj = session.query(mapcls).filter(mapcls.id ==i[0]).one()
            setattr(recorder,i[2],linkobj)
        for i in asso_tables:
            mapcls = i[1]
            #主键到map对象(表记录) 的map function 
            objs = []
            for j in i[0]:
                objs.append(session.query(mapcls).filter(mapcls.id ==j).one())                
            if bool(objs):setattr(recorder,i[2],objs)
        session.add(recorder)
        
        for i in asso_obj_tables:
            mapcls = i[1]
            #主键到map对象(表记录) 的map function
            obj1 = session.query(mapcls).filter(mapcls.id ==i[0]).one()
            obj2 = recorder
            setvalues = i[5]
            #add source obj
            setvalues[i[2]] = obj1
            # add target obj
            setvalues[i[4]]= obj2
            # instance association obj
            link_obj = i[3]()
            for kw in setvalues.keys():
                setattr(link_obj,kw,setvalues[kw])
            #submit to db
            session.add(link_obj)                   
        try:
            session.commit()
#             self.fire_event(RecorderCreated,recorder)
        except:
            session.rollback()
            raise
        finally:
            session.close()                        

    def fire_event(self,eventcls,recorder):
            if getattr(recorder,'id','') == '':return
            cls = "xtcs.policy.%s" % self.table
            ttl = getattr(recorder,'mingcheng',u'') or getattr(recorder,'xingming',u'') or \
             getattr(recorder,'xing',u'') or getattr(recorder,'wei',u'')
            eventobj = eventcls(id=recorder.id,cls=cls,ttl=ttl) 
            if eventobj.available():event.notify(eventobj)               
    
    def update_multi_tables(self,kwargs,fk_tables=[],asso_tables=[],asso_obj_tables=[]):
        "更新本表的同时,兼顾处理外键表,关联表,关联对象表"
        "fk_tables:[(pk,map_cls,attr),...]"
        "asso_tables:[([pk1,pk2,...],map_cls,attr),...]"
        """asso_obj_tables:{"asso_proxy_property1":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]),...],
                            "asso_proxy_property2":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]]
                            ,...}"""
        
        id = kwargs['id']
        if bool(id):
            tablecls = self.init_table()
            try:
                recorder = self.getByCode(id)
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'id']
                for kw in updatedattrs:
                    setattr(recorder,kw,kwargs[kw])
                for i in fk_tables:
                    mapcls = i[1]
                    linkobj = session.query(mapcls).filter(mapcls.id ==i[0]).one()
                    setattr(recorder,i[2],linkobj)
                for i in asso_tables:                    
                    mapcls = i[1]
                    objs = []
                    for j in i[0]:
                        objs.append(session.query(mapcls).filter(mapcls.id ==j).one())                
                    if bool(objs):setattr(recorder,i[2],objs)
                session.add(recorder)        
                if bool(asso_obj_tables):
                    keys = asso_obj_tables.keys()
                else:
                    keys = []  
                for kw in keys:
                    link_objs = []
                    for i in asso_obj_tables[kw]:
                    # i like as:(pk,pk_cls,pk_attr,asso_cls,asso_attr,ppt)
                    # many to many association object table,update recorder
                    #first locate the recorder by two FK
                        src_id = "%s_id" % i[2]
                        self_id = "%s_id" % i[4]
                        kwargs = i[5]                    
                        cns = {src_id:i[0],self_id:recorder.id}                 
                        pkobj = session.query(i[1]).filter(i[1].id ==i[0]).one()
                        # check if the association recorder is existed
                        asso_obj = self.get_asso_obj(cns,i[3])
                        if bool(asso_obj):
                        # this is old recorder,just update it
#                         updatedattrs = [kw for kw in kwargs.keys() if kw != self_id]
                            for kw in kwargs.keys():
                                setattr(asso_obj,kw,kwargs[kw])                        
                        else:
                        # this is new association recorder,we will create it
                            setvalues = i[5]
            #add source obj
                            setvalues[i[2]] = pkobj
            # add target obj
                            setvalues[i[4]]= recorder
            # instance association obj
                            asso_obj = i[3]()
                            for kw in setvalues.keys():
                                setattr(asso_obj,kw,setvalues[kw])                      
                        session.add(asso_obj)
                        link_objs.append(pkobj)
                    # update association proxy property
                    setattr(recorder,kw,link_objs)
#                     session.add(recorder) 
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()                
        else:
            pass    
    
    def update_asso_table(self,kwargs,searchcnd):
        """
        data:will be update data :type dict
        searchcnd:the search condition that located the recorder type: dict
        """
        if bool(searchcnd):
            recorder = self.getByKwargs(**searchcnd)
            try:
                updatedattrs = [kw for kw in kwargs.keys()]
                for kw in updatedattrs:
                    setattr(recorder,kw,kwargs[kw])                
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()                
                        
    def query(self,kwargs):
        """分页查询
        kwargs's keys parameters:
        start:start location
        size:batch size
        keyword:full search keyword
        direction:sort direction
        max:batch size for Oracle
        with_entities:if using serial number fetch recorder's columns,1 True,0 False      
        """        
        tablecls = self.init_table()        
        start = int(kwargs['start']) 
        size = int(kwargs['size'])
        max = size + start + 1
        keyword = kwargs['SearchableText']        
        direction = kwargs['sort_order'].strip()
        try:
            with_entities = kwargs['with_entities']
        except:
            kwargs['with_entities'] = 1
            with_entities = 1                                       
        if size != 0:
            if keyword == "":
                if direction == "reverse":
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s ORDER BY id DESC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % self.table
                    else:                            
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s 
                         ORDER BY id DESC limit :start,:max""" % self.table                    
                    selectcon = text(sqltext)
                else:
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s ORDER BY id ASC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % self.table
                    else:                  
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s 
                         ORDER BY id ASC limit :start,:max""" % self.table                                        
                    selectcon = text(sqltext)                    
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(start=start,max=max)).all()
                    except:
                        session.rollback()
                elif linkstr.startswith("oracle"):
                    try:
                        recorders = session.query(tablecls).\
                    order_by(tablecls.id.desc()).all()[start:max]
                    except:
                        session.rollback()
                else:
                    try:
                        recorders = session.query(tablecls).\
                    order_by(tablecls.id.desc()).limit(max).offset(start)
                    except:
                        session.rollback()                    
            else:
                keysrchtxt = self.search_clmns2sqltxt(self.fullsearch_clmns)
                if direction == "reverse":
                    if linkstr.startswith("oracle"):                                                                
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %(tbl)s WHERE %(ktxt)s  ORDER BY id DESC ) a 
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,ktxt=keysrchtxt)
                    else:
                        max = max - 1
                        sqltext = """SELECT * FROM %(tbl)s
                        WHERE %(ktxt)s 
                        ORDER BY id DESC limit :start,:max
                         """ % dict(tbl=self.table,ktxt=keysrchtxt)                        
                    selectcon = text(sqltxt)
                else:
                    if linkstr.startswith("oracle"):                     
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %(tbl)s WHERE %(ktxt)s  ORDER BY id ASC ) a 
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,ktxt=keysrchtxt)
                    else:
                        max = max - 1
                        sqltxt = """SELECT * FROM %(tbl)s
                        WHERE %(ktxt)s 
                        ORDER BY id ASC limit :start,:max
                         """ % dict(tbl=self.table,ktxt=keysrchtxt)                                                                 
                    selectcon = text(sqltxt)
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(x=keyword,start=start,max=max)).all()
                    except:
                        session.rollback()
                elif linkstr.startswith("oracle"):
                    try:
                        recorders = session.query(tablecls).\
                    order_by(tablecls.id.desc()).all()[start:max]
                    except:
                        session.rollback()                                    
                else:
                    try:
                        recorders = session.query(tablecls).\
                    order_by(tablecls.id.desc()).limit(max).offset(start)
                    except:
                        session.rollback()
            try:
                if not bool(recorders):
                    recorders = []
            except:
                recorders = []
            return recorders
        else:
            if keyword == "":
                selectcon = text("SELECT * FROM %s ORDER BY id DESC " % self.table)
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon).all()
                    except:
                        session.rollback()
                else:
                    try:
                        recorders = session.query(tablecls).\
                    order_by(tablecls.id.desc()).all()
                    except:
                        session.rollback()                    
            else:
                keysrchtxt = self.search_clmns2sqltxt(self.fullsearch_clmns)
                sqltext = """SELECT * FROM %(tbl)s WHERE %(ktxt)s  
                 ORDER BY id DESC """ % dict(tbl=self.table,ktxt=keysrchtxt)
                selectcon = text(sqltext)                
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(x=keyword)).all()
                    except:
                        session.rollback()
                else:
                    keysearchcnd = self.search_clmns4filter(self.fullsearch_clmns,tablecls,keyword)
                    if bool(keysearchcnd):
                        if len(keysearchcnd) > 1:
                            try:
                                recorders = session.query(tablecls).filter(or_(*keysearchcnd)). \
                    order_by(tablecls.id.desc()).all()
                            except:
                                session.rollback()
                        else:
                            try:
                                recorders = session.query(tablecls).filter(keysearchcnd[0]). \
                    order_by(tablecls.id.desc()).all()
                            except:
                                session.rollback()                                                                                  
                    else:
                        try:
                            recorders = session.query(tablecls).order_by(tablecls.id.desc()).all()
                        except:
                            session.rollback()                                                                                                  
            
            if bool(recorders):
                nums = len(recorders)
            else:
                nums = 0
            return nums

    def filter_args2sql(self,filter_args):
        """filter parameters dic transfer to sql where statement
        input:{"did":21,"state":0}
        output: "did = 21 AND state =0"
        """
        items = [[k,v] for k,v in filter_args.iteritems()]
        out = map(lambda x:"%s = %s" % (x[0],x[1]) ,items)

        return ' AND '.join(out)

    def filter_args2ormfilter(self,filter_args):
        """filter parameters dic transfer to sql where statement
        input:{"did":21,"state":0}
        output: [getattr(tablecls,did) == 21,getattr(tablecls,state) == 0]
        """
        tablecls = self.init_table()
        items = [[k,v] for k,v in filter_args.iteritems()]
        out = map(lambda x:getattr(tablecls,x[0]) == x[1] ,items)
       
        return out         
    
    def query_with_filter(self,kwargs,filter_args):
        """分页查询
        kwargs's keys parameters:
        start:start location
        size:batch size
        keyword:full search keyword
        direction:sort direction
        max:batch size for Oracle
        with_entities:if using serial number fetch recorder's columns,1 True,0 False      
        """        
        tablecls = self.init_table()        
        start = int(kwargs['start']) 
        size = int(kwargs['size'])
        max = size + start + 1
        keyword = kwargs['SearchableText']
        orderby = kwargs['order_by']        
        direction = kwargs['sort_order'].strip()
        import pdb
        pdb.set_trace()        
        try:
            with_entities = kwargs['with_entities']
        except:
            kwargs['with_entities'] = 1
            with_entities = 1                                       
        if size != 0:
            if keyword == "":
                if direction == "reverse":
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s WHERE %s ORDER BY %s DESC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % (self.table,
                                                                 self.filter_args2sql(filter_args),
                                                                 orderby)
                    else:                            
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s WHERE %s 
                         ORDER BY %s DESC limit :start,:max""" % (self.table,
                                                                  self.filter_args2sql(filter_args),
                                                                  orderby)                    
                    selectcon = text(sqltext)
                else:
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s WHERE %s ORDER BY %s ASC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % (self.table,
                                                                 self.filter_args2sql(filter_args),
                                                                 orderby)
                    else:                  
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s WHERE %s 
                         ORDER BY %s ASC limit :start,:max""" % (self.table,
                                                                 self.filter_args2sql(filter_args),
                                                                 orderby)                                        
                    selectcon = text(sqltext)                    
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(start=start,max=max)).all()
                    except:
                        session.rollback()
                elif linkstr.startswith("oracle"):
                    ftrclmns = self.filter_args2ormfilter(filter_args)
                    try:
                        recorders = session.query(tablecls).filter(*ftrclmns).\
                    order_by(getattr(tablecls,orderby).desc()).all()[start:max]
                    except:
                        session.rollback()
                else:
                    ftrclmns = self.filter_args2ormfilter(filter_args)
                    try:
                        recorders = session.query(tablecls).filter(*ftrclmns).\
                    order_by(getattr(tablecls,orderby).desc()).limit(max).offset(start)
                    except:
                        session.rollback()                    
            else:
                keysrchtxt = self.search_clmns2sqltxt(self.fullsearch_clmns)
                if direction == "reverse":
                    if linkstr.startswith("oracle"):                                                                
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %(tbl)s WHERE %(ktxt)s AND %(filter_cols)s ORDER BY %(orderby)s DESC ) a 
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,
                               ktxt=keysrchtxt,
                               filter_cols=self.filter_args2sql(filter_args),
                               orderby=orderby)
                    else:
                        max = max - 1
                        sqltext = """SELECT * FROM %(tbl)s
                        WHERE %(ktxt)s AND %(filter_cols)s 
                        ORDER BY %(orderby)s DESC limit :start,:max
                         """ % dict(tbl=self.table,
                                    ktxt=keysrchtxt,
                                    filter_cols=self.filter_args2sql(filter_args),
                                    orderby=orderby)                        
                    selectcon = text(sqltxt)
                else:
                    if linkstr.startswith("oracle"):                     
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %(tbl)s WHERE %(ktxt)s AND %(filter_cols)s ORDER BY %(orderby)s ASC ) a 
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,
                               ktxt=keysrchtxt,
                               filter_cols=self.filter_args2sql(filter_args),
                               orderby=orderby)
                    else:
                        max = max - 1
                        sqltxt = """SELECT * FROM %(tbl)s
                        WHERE %(ktxt)s AND %(filter_cols)s 
                        ORDER BY %(orderby)s ASC limit :start,:max
                         """ % dict(tbl=self.table,
                                    ktxt=keysrchtxt,
                                    filter_cols=self.filter_args2sql(filter_args),
                                    orderby=orderby)                                                                 
                    selectcon = text(sqltxt)
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(x=keyword,start=start,max=max)).all()
                    except:
                        session.rollback()
                elif linkstr.startswith("oracle"):
                    ftrclmns = self.filter_args2ormfilter(filter_args)
                    try:
                        recorders = session.query(tablecls).filter(*ftrclmns).\
                    order_by(getattr(tablecls,orderby).desc()).all()[start:max]
                    except:
                        session.rollback()                                    
                else:
                    ftrclmns = self.filter_args2ormfilter(filter_args)
                    try:
                        recorders = session.query(tablecls).filter(*ftrclmns).\
                    order_by(getattr(tablecls,orderby).desc()).limit(max).offset(start)
                    except:
                        session.rollback()
            try:
                if not bool(recorders):
                    recorders = []
            except:
                recorders = []
            return recorders
        else:
            if keyword == "":
                selectcon = text("SELECT * FROM %s WHERE %s " % (self.table,self.filter_args2sql(filter_args)))
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon).all()
                    except:
                        session.rollback()
                else:
                    ftrclmns = self.filter_args2ormfilter(filter_args)
                    try:
                        recorders = session.query(tablecls).filter(*ftrclmns).all()
                    except:
                        session.rollback()                    
            else:
                keysrchtxt = self.search_clmns2sqltxt(self.fullsearch_clmns)
                sqltext = """SELECT * FROM %(tbl)s WHERE %(ktxt)s AND %(filter_cols)s  
                 """ % dict(tbl=self.table,ktxt=keysrchtxt,filter_cols=self.filter_args2sql(filter_args))
                selectcon = text(sqltext)                
                if bool(with_entities):
                    clmns = self.get_columns()
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(x=keyword)).all()
                    except:
                        session.rollback()
                else:
                    ftrclmns = self.filter_args2ormfilter(filter_args)
                    keysearchcnd = self.search_clmns4filter(self.fullsearch_clmns,tablecls,keyword)
                    if bool(keysearchcnd):
                        if len(keysearchcnd) > 1:
                            try:
                                recorders = session.query(tablecls).filter(or_(*keysearchcnd)). \
                    filter(*ftrclmns).all()
                            except:
                                session.rollback()
                        else:
                            try:
                                recorders = session.query(tablecls).filter(keysearchcnd[0]). \
                    filter(*ftrclmns).all()
                            except:
                                session.rollback()                                                                                  
                    else:
                        try:
                            recorders = session.query(tablecls).filter(*ftrclmns).all()
                        except:
                            session.rollback()                                                                                                  
            
            if bool(recorders):
                nums = len(recorders)
            else:
                nums = 0
            return nums
    
    def multi_query(self,kwargs,tmaper,tbl,tc,cv,key1,key2):
        """多表连接分页查询
        kwargs's keys parameters:
        start:start location
        size:batch size
        keyword:full search keyword
        direction:sort direction
        max:batch size for Oracle
        with_entities:if using serial number fetch recorder's columns,1 True,0 False
        tmaper: will joined table's mapper object
        tbl: will joined table's name
        tc:will be checked table column
        cv:the tc should equal value
        key1:first table primary key
        key:second table fk's refer to first table     
        """        
        tablecls = self.init_table()        
        start = int(kwargs['start']) 
        size = int(kwargs['size'])
        max = size + start + 1
        keyword = kwargs['SearchableText']        
        direction = kwargs['sort_order'].strip()

        try:
            with_entities = kwargs['with_entities']
        except:
            kwargs['with_entities'] = 1
            with_entities = 1                                       
        if size != 0:
            if keyword == "":
                if direction == "reverse":
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s JOIN %s WHERE %s = %s AND %s = %s ORDER BY id DESC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % (self.table,tbl,tc,cv,key1,key2)
                    else:                            
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s JOIN %s WHERE %s = %s AND %s = %s
                         ORDER BY id DESC limit :start,:max""" % (self.table,tbl,tc,cv,key1,key2)                    
                    selectcon = text(sqltext)
                else:
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s JOIN %s WHERE %s = %s AND %s = %s ORDER BY id ASC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % (self.table,tbl,tc,cv,key1,key2)
                    else:                  
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s JOIN %s WHERE %s = %s AND %s = %s 
                         ORDER BY id ASC limit :start,:max""" % (self.table,tbl,tc,cv,key1,key2)                                       
                    selectcon = text(sqltext)                    
                if bool(with_entities):
                    clmns = self.join_columns(tmaper)
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(start=start,max=max)).all()
                    except:
                        session.rollback()
                        return []
                else:
                    try:
                        recorders = session.query(tablecls).\
                            from_statement(selectcon.params(start=start,max=max)).all()
                    except:
                        session.rollback()
                        return []                    
            else:
                keysrchtxt = self.search_clmns2sqltxt(self.fullsearch_clmns)
                if direction == "reverse":
                    if linkstr.startswith("oracle"):                                                                
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
(SELECT * FROM %(tbl)s JOIN %(tbl2)s WHERE %(ktxt)s AND %(tc)s = %(cv)s  AND %(key1)s = %(key2)s ORDER BY id DESC ) a 
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,ktxt=keysrchtxt,tbl2=tbl,tc=tc,cv=cv,key1=key1,key2=key2)
                    else:
                        max = max - 1
                        sqltext = """SELECT * FROM %(tbl)s JOIN %(tbl2)s
                        WHERE %(ktxt)s AND %(tc)s = %(cv)s AND %(key1)s = %(key2)s 
                        ORDER BY id DESC limit :start,:max
                         """ % dict(tbl=self.table,ktxt=keysrchtxt,tbl2=tbl,tc=tc,cv=cv,key1=key1,key2=key2)                        
                    selectcon = text(sqltxt)
                else:
                    if linkstr.startswith("oracle"):                     
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
(SELECT * FROM %(tbl)s JOIN %(tbl2)s WHERE %(ktxt)s AND %(tc)s = %(cv)s AND %(key1)s = %(key2)s ORDER BY id ASC ) a  
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,ktxt=keysrchtxt,tbl2=tbl,tc=tc,cv=cv,key1=key1,key2=key2)
                    else:
                        max = max - 1
                        sqltext = """SELECT * FROM %(tbl)s JOIN %(tbl2)s
                        WHERE %(ktxt)s AND %(tc)s = %(cv)s AND %(key1)s = %(key2)s 
                        ORDER BY id ASC limit :start,:max
                         """ % dict(tbl=self.table,ktxt=keysrchtxt,tbl2=tbl,tc=tc,cv=cv,key1=key1,key2=key2)                                                                 
                    selectcon = text(sqltxt)
                if bool(with_entities):
                    clmns = self.join_columns(tmaper)
                    try:
                        recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(x=keyword,start=start,max=max)).all()
                    except:
                        session.rollback()
                        return []
                else:
                    try:
                        recorders = session.query(tablecls).\
                            from_statement(selectcon.params(x=keyword,start=start,max=max)).all()
                    except:
                        session.rollback()
                        return []
            return recorders
# return total
        else:
            if keyword == "":               
                try:
                    recorders = session.query(tablecls).join(tmaper,getattr(tmaper,tc)==cv).\
                    filter(getattr(tablecls,key1)==getattr(tmaper,key2)).all()
                except:
                    session.rollback()
                    recorders = []                  
            else:
                keysearchcnd = self.search_clmns4filter(self.fullsearch_clmns,tablecls,keyword)
                if bool(keysearchcnd):
                    if len(keysearchcnd) > 1:
                        try:
                            recorders = session.query(tablecls).join(tmaper,getattr(tmaper,tc)==cv).\
                                filter(getattr(tablecls,key1)==getattr(tmaper,key2)).filter(or_(*keysearchcnd)).all()
                        except:
                            session.rollback()
                            recorders = []
                    else:
                        try:
                            recorders = session.query(tablecls).join(tmaper,getattr(tmaper,tc)==cv).\
                                filter(getattr(tablecls,key1)==getattr(tmaper,key2)).filter(keysearchcnd[0]).all()
                        except:
                            session.rollback()
                            recorders = []                                                                                  
                else:
                    try:
                        recorders = session.query(tablecls).join(tmaper,getattr(tmaper,tc)==cv).\
                            filter(getattr(tablecls,key1)==getattr(tmaper,key2)).all()
                    except:
                        session.rollback()
                        recorders = []                                                                                             
            
            if bool(recorders):
                nums = len(recorders)
            else:
                nums = 0
            return nums
            
    
    def init_table(self):
        "import table class"
        if isinstance(self.factorycls,str):
            import_str = "from %(p)s import %(t)s as tablecls" % dict(p=self.package,t=self.factorycls) 
            exec import_str
            return tablecls
        else:
            return self.factorycls          
    
    def deleteByKwargs(self,**args):
        ""
        tablecls = self.init_table()       
        if bool(args):           
            try:
                args2 = ["%s = %s" %(kw,vl) for kw,vl in args.items()]
                args2 = map(text,args2)
                recorder = session.query(tablecls).filter(and_(*args2)).first()
                session.delete(recorder)
                session.commit()
                rt = True
            except:
                session.rollback()
                rt = sys.exc_info()[1]
            finally:
                session.close()
                return rt
        else:
            return "id can't be empty"        

    def DeleteByCode(self,id,pk=None):
        "delete the specify id recorder"

        if not bool(id): return "id can't be empty"
        if not bool(pk): 
            try:
                recorder = self.getByCode(id)                
                session.delete(recorder)
                session.commit()
#                 self.fire_event(RecorderDeleted,recorder)
                rt = True
            except:
                session.rollback()
                rt = sys.exc_info()[1]
            finally:
                session.close()
                return rt
        else:
            try:
                recorder = self.getByCode(id,pk)                
                session.delete(recorder)
                session.commit()
#                 self.fire_event(RecorderDeleted,recorder)
                rt = True
            except:
                session.rollback()
                rt = sys.exc_info()[1]
            finally:
                session.close()
                return rt            

    def updateByCode(self,kwargs):
        "update the speicy table recorder"

        id = kwargs['id']
        if not bool(id): return None
        if "pk" not in kwargs:               
            try:
                recorder = self.getByCode(id)
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'id']
                for kw in updatedattrs:
                    setattr(recorder,kw,kwargs[kw])
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()                
        else:
            try:
                recorder = self.getByCode(id,kwargs['pk'])
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'pk' and kw != 'id']
                for kw in updatedattrs:
                    setattr(recorder,kw,kwargs[kw])
                session.commit()
            except:
                session.rollback()
            finally:
                session.close() 

    def getByCode(self,id,pk=None):
        
        tablecls = self.init_table()        
        if not bool(id):return None          
        if not bool(pk):
            try:
                recorder = session.query(tablecls).\
                filter(tablecls.id == id).one()
                return recorder
            except:
                session.rollback()
                return None
        else:
            try:
                recorder = session.query(tablecls).\
                filter(getattr(tablecls,pk) == id).one()
                return recorder
            except:
                session.rollback()
                return None

    def getByKwargs(self,**args):
        
        tablecls = self.init_table()
     
        if bool(args):           
            try:
                args2 = ["%s = %s" %(kw,vl) for kw,vl in args.items()]
                args2 = map(text,args2)
                recorder = session.query(tablecls).filter(and_(*args2)).first()
                return recorder
            except:
                session.rollback()
                return None
        else:
            return None

    def getMultiByKwargs(self,**args):
        
        tablecls = self.init_table()       
        if bool(args):           
            try:
                args2 = ["%s = %s" %(kw,vl) for kw,vl in args.items()]
                args2 = map(text,args2)
                recorders = session.query(tablecls).filter(and_(*args2)).all()
                return recorders
            except:
                session.rollback()
                return []
            finally:
                session.close()
                
        else:
            return []
    
    def get_rownumber(self):
        "fetch table's rownumber"
#         query = "SELECT COUNT(*) FROM %(table)s;" % dict(table=self.table)
        tablecls = self.init_table()
        try:
            num = self.session.query(func.count(tablecls.id)).scalar()         
            return num
        except:
            self.session.rollback()
            return 0            

    def fetch_oldest(self):
        "delete from(select * from <table_name>) where rownum<=1000;"
        
        s = self.session
        sql2 = """ 
        SELECT datetime FROM (
          SELECT * FROM %(tbl)s ORDER BY id ASC
         )
          WHERE rownum<= 1
        """ % dict(tbl=self.table)
        query2 = text(sql2)                                                                                                
        try:
            rownum = s.execute(query2).fetchone()
            if len(rownum):
                return datetime.strptime(rownum[0],fmt) 
            else:
                return datetime.datetime.now()
#             s.commit()
        except:
            s.rollback()
            return datetime.datetime.now()
    
    def bulk_delete(self,size):
        "delete from(select * from <table_name>) where rownum<=1000;"
        
        s = self.session
        sql2 = """
        DELETE %(tbl)s
         WHERE  id in (
        SELECT id FROM (
          SELECT * FROM %(tbl)s ORDER BY id ASC
         )
          WHERE rownum<= :max
        )
        """ % dict(tbl=self.table)
        query2 = text(sql2).params(max=size)                                                                                                 
        try:
            rownum = s.execute(query2)
            s.commit()
        except:
            s.rollback()
        finally:
            s.close()


