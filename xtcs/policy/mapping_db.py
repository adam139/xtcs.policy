#-*- coding: UTF-8 -*-
import sqlalchemy.schema
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql
from datetime import datetime
from zope import schema
from zope.interface import Interface,implements
from xtcs.policy import ORMBase,engine
from xtcs.policy import _

def nowDateTime():
    return datetime.today()

# automap
metadata = MetaData()
metadata.reflect(engine, only=['accesstoken','xiangmu','juanzeng'])
AutoBase = automap_base(metadata=metadata)
AutoBase.prepare()
# OnlinePay = AutoBase.classes.onlinepay
AccessToken = AutoBase.classes.accesstoken
XiangMu = AutoBase.classes.xiangmu
JuanZeng = AutoBase.classes.juanzeng


         

class IJuanZeng(Interface):
    """donor 记录在某一慈善项目（did决定）下，所有捐赠记录
| id               | int(10) unsigned | NO   | PRI | NULL              | auto_increment |
| xiangmu_id       | int(10) unsigned | NO   | MUL | NULL              |                |
| xingming         | varchar(64)      | NO   | MUL |                   |                |
| xianjin          | decimal(13,2)    | NO   |     | 0.00              |                |
| wuzi             | varchar(128)     | NO   |     |                   |                |
| wuzi_jiazhi      | decimal(13,2)    | NO   |     | 0.00              |                |
| juanzeng_shijian | datetime         | NO   |     | CURRENT_TIMESTAMP |                |
| openid           | varchar(128)     | NO   | MUL | noweixin          |                |
| status           | tinyint(1)       | NO   |     | 0                 | 

    """
    id = schema.Int(
            title=_(u"table primary key"),
        )          
    xiangmu_id = schema.Choice(
            title=_(u"juanzeng xiangmu id"),
            vocabulary='xtcs.policy.vocabulary.donateId',
            required=True,
        )
    xingming = schema.TextLine(
            title=_(u"juanzeng zhe"),
        )
    xianjin = schema.Float(
            title=_(u"xianjin jin e"),            
            required=False
        )
    wuzi = schema.TextLine(
            title=_(u"juanzeng wuping"),
            required=False
        )
    wuzi_jiazhi = schema.Float(
            title=_(u"wuzi jiazhi"),            
            required=False
        )                
    juanzeng_shijian = schema.Datetime(
            title=_(u"juanzeng shi jian"),
            defaultFactory=nowDateTime
        )
    openid = schema.TextLine(
            title=_(u"weixin openid"),
            required=False
#             default = "noweixinpay"
        )
    status = schema.Int(
            title=_(u"yidong zhifu zhuangtai"),
            required=False,
            default = 1
        )        
    
class JuanZeng(ORMBase):
    """Database-backed implementation of project
    """
    implements(IJuanZeng)
    __tablename__ = 'juanzeng'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
    xiangmu_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )    

    xingming = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    xianjin = sqlalchemy.schema.Column(sqlalchemy.types.Float(13,2),
            nullable=False,
            default=0.00
        )
    wuzi = sqlalchemy.schema.Column(sqlalchemy.types.String(64),
            nullable=False, 
        )
    wuzi_jiazhi = sqlalchemy.schema.Column(sqlalchemy.types.Float(13,2),
            nullable=False,
            default=0.00
        )    
    juanzeng_shijian = sqlalchemy.schema.Column(sqlalchemy.types.DateTime(),
            nullable=True,
        )
    openid = sqlalchemy.schema.Column(sqlalchemy.types.String(128),
            nullable=False,
        )    
    status = sqlalchemy.schema.Column(sqlalchemy.types.SmallInteger(),
            nullable=False,
        )

#所有有捐赠记录的项目,捐赠公示
class IXiangMu(Interface):
    """捐赠项目
    mysql> describe xiangmu;
 id           | int(10) unsigned | NO   | PRI | NULL              | auto_increment |
| mingcheng    | varchar(64)      | NO   | MUL |                   |                |
| jieshao      | varchar(256)     | NO   |     |                   |                |
| zhuceshijian | datetime         | NO   |     | CURRENT_TIMESTAMP |                |
| youxiao      | tinyint(1)       | NO   |     | 1                 |                |
+--------------+------------------+------+-----+-------------------+----------------+
    
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )
    mingcheng = schema.TextLine(
            title=_(u"cishan juanzeng xiangmu mingcheng"),
        )    
    jieshao = schema.Text(
            title=_(u"cishan juanzeng xiangmu beizhu"),
            required=False
        )
    zhuceshijian = schema.Datetime(
            title=_(u"kaishi shijian"),
            defaultFactory=nowDateTime            
        )           
    youxiao = schema.Int(
            title=_(u"shifou keshi?"),
            default=0
        )

class XiangMu(ORMBase):
    """Database-backed implementation of project
    """
    implements(IXiangMu)
    __tablename__ = 'xiangmu'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
    mingcheng = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    jieshao = sqlalchemy.schema.Column(sqlalchemy.types.String(64),
            nullable=True,
        )
    zhuceshijian = sqlalchemy.schema.Column(sqlalchemy.types.DateTime(),
            nullable=False,
        )
    youxiao = sqlalchemy.schema.Column(sqlalchemy.types.SmallInteger(),
            nullable=False,
        )
