# -*- coding: utf-8 -*-
from xtcs.policy import engine
from xtcs.policy import fmt
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, desc,asc       

from Products.CMFPlone.utils import safe_unicode
from xtcs.policy.interfaces import IDbapi
from zope.component import queryUtility
from datetime import datetime,timedelta
       
def import_contents(context):
    "copy mysql db table 'donate' to table 'xiangmu'"
    
      
    
    def query(kwargs):
        """
        mysql> select pid from plone_forum_post limit 2 offset 1;

        """
        size = kwargs['size']
        offset = kwargs['offset']
        with engine.connect() as con:
            meta = MetaData(engine)
            src_table = Table('donate', meta, autoload=True)
            stm = select([src_table.c.aname, src_table.c.amemo, src_table.c.visible, src_table.c.start_time])\
            .where(src_table.c.aname !=u"").order_by(asc(src_table.c.did)).limit(size).offset(offset)
            rs = con.execute(stm)
        return rs.fetchall()
    
    recorders = query({"size":8,"offset":0})
    locator = queryUtility(IDbapi, name='xiangmu')
    for j in recorders:
        data = {}
        data['mingcheng'] = j[0]
        data['jieshao'] = j[1]               
        data['youxiao'] = j[2]
        data['zhuceshijian'] = datetime.utcfromtimestamp(j[3])               
        try:
            locator.add(data)
        except:
            continue
    return        


def cp_donor2juanzeng(context):
    "copy mysql db table 'donor' to table 'juanzeng'"
    """
    select doid,aname,money from donor 
    where money != NULL or money !="" 
    order by doid asc limit 2 offset 0;
    
    select doid,aname,money,goods from donor 
    where goods != NULL or goods !="" 
    order by doid asc limit 12 offset 0;
    
    select doid,aname,money,goods from donor 
    where (goods != NULL or goods !="") and (money != NULL or money !="") 
    order by doid asc limit 12 offset 0;
    """
    
      
    
    def query(kwargs):
        """
        mysql> select pid from plone_forum_post limit 2 offset 1;

        """
        size = kwargs['size']
        offset = kwargs['offset']
        with engine.connect() as con:
            meta = MetaData(engine)
            src_table = Table('donor', meta, autoload=True)
            stm = select([src_table.c.did, src_table.c.aname, src_table.c.money, src_table.c.goods, src_table.c.atime])\
            .where(src_table.c.aname !=u"").order_by(asc(src_table.c.did)).limit(size).offset(offset)
            rs = con.execute(stm)
        return rs.fetchall()
    
    recorders = query({"size":700,"offset":0})
    locator = queryUtility(IDbapi, name='juanzeng')
    #old and new table xiangmu'id map
    idmap = {7:6,12:7,13:8,18:9,21:10,22:11}
    import re
    
    for j in recorders:
        data = {}
        data['xiangmu_id'] = idmap[int(j[0])]
        data['xingming'] = j[1].strip()
        xianjin = j[2]
        if bool(xianjin): 
            if xianjin.isdecimal():               
                data['xianjin'] = float(xianjin)
        wuzi = j[3]
        if bool(wuzi):
            wz = wuzi.split(',')
            if wuzi.isdecimal():               
                data['wuzi_jiazhi'] = float(wuzi)
                data['wuzi'] = "价值{0}元物资".format(wuzi).encode('utf-8')        
             
            elif len(wz) > 1:
                wuzijiazhi =  re.findall(r'\d+',wz[-1])
                if bool(wuzijiazhi):
                    data['wuzi_jiazhi'] = float(wuzijiazhi[0])
                    data['wuzi'] = wuzi                

            elif len(wz) == 1:
                s5 = u"\uff0c"
                wz= wuzi.split(s5)
                if len(wz) > 1:                
                    wuzijiazhi =  re.findall(r'\d+',wz[-1])
                    if bool(wuzijiazhi):
                        data['wuzi_jiazhi'] = float(wuzijiazhi[0])
                        data['wuzi'] = wuzi
                else:                        
                    data['wuzi'] = wuzi        
        data['status'] = 1
        shijian = j[4]

        if bool(shijian) and isinstance(shijian,datetime):
            data['juanzeng_shijian'] = shijian
        elif isinstance(shijian,int):
            data['juanzeng_shijian'] = datetime.utcfromtimestamp(shijian)
        else:
            data['juanzeng_shijian'] = datetime.strptime("2000-01-01 00:00:00",fmt)                                          
        try:
#             pass
            locator.add(data)
        except:
            continue
    return                         