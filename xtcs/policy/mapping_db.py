#-*- coding: UTF-8 -*-
# import xtcs.policy.types
import sqlalchemy.schema
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import Interface,implements
from xtcs.policy import ORMBase,engine
from xtcs.policy import _

def nowDateTime():
    return datetime.today()

# automap
metadata = MetaData()
metadata.reflect(engine, only=['onlinepay','accesstoken','xiangmu','juanzeng'])
AutoBase = automap_base(metadata=metadata)
AutoBase.prepare()
OnlinePay = AutoBase.classes.onlinepay
AccessToken = AutoBase.classes.accesstoken
XiangMu = AutoBase.classes.xiangmu
JuanZeng = AutoBase.classes.juanzeng


class IArticle(Interface):
    """慈善文摘
    select pubtime,title,content from article where id = 199
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )
    sortparentid = schema.Int(
            title=_(u"main folder id"),
        )
    sortchildid = schema.Int(
            title=_(u"sub folder id"),
        )        
    pubtime = schema.Date(
            title=_(u"fabu ri qi")
        )
    title = schema.TextLine(
            title=_(u"wenzhang biaoti"),
        )    
    content = schema.TextLine(
            title=_(u"wenzhang neirong"),
        )


class Article(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IArticle)

    __tablename__ = 'article'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
    sortparentid = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )
    sortchildid = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )    
    pubtime = sqlalchemy.schema.Column(sqlalchemy.types.Date(),
            nullable=False,
        )
    title = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    content = sqlalchemy.schema.Column(mysql.LONGTEXT,
            nullable=False,
        )

class IProject(Interface):
    """慈善项目
    id,projectName,registertime,description
    select pubtime,title,content from article where id = 199
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )       
    registertime = schema.Date(
            title=_(u"dengji ri qi")
        )
    projectName = schema.TextLine(
            title=_(u"xiangmu mingcheng"),
        )    
    description = schema.Text(
            title=_(u"xiangmu miaoshu"),
        )


class Project(ORMBase):
    """Database-backed implementation of project
    """
    implements(IProject)

    __tablename__ = 'project'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
    
    registertime = sqlalchemy.schema.Column(sqlalchemy.types.Date(),
            nullable=False,
        )
    projectName = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    description = sqlalchemy.schema.Column(mysql.LONGTEXT,
            nullable=False,
        )

class IVolunteerteam(Interface):
    """义工团队
    id,projectName,registertime,description
    select pubtime,title,content from article where id = 199
    +--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int(10)      | NO   | PRI | NULL    | auto_increment |
| teamName     | varchar(32)  | NO   |     | NULL    |                |
| imagepath    | varchar(255) | YES  |     | NULL    |                |
| description  | varchar(200) | YES  |     | NULL    |                |
| volunteerNum | int(10)      | YES  |     | NULL    |                |
| registertime | int(10)      | NO   |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+

    """
    id = schema.Int(
            title=_(u"table primary key"),
        )       
    registertime = schema.Date(
            title=_(u"dengji ri qi")
        )
    teamName = schema.TextLine(
            title=_(u"yigong tuandui mingcheng"),
        )    
    description = schema.Text(
            title=_(u"yigong tuandui jieshao"),
        )


class Volunteerteam(ORMBase):
    """Database-backed implementation of project
    """
    implements(IVolunteerteam)

    __tablename__ = 'volunteerteam'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
    
    registertime = sqlalchemy.schema.Column(sqlalchemy.types.Date(),
            nullable=False,
        )
    teamName = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    description = sqlalchemy.schema.Column(mysql.LONGTEXT,
            nullable=False,
        )
    
class IDonor(Interface):
    """donor 记录在某一慈善项目（did决定）下，所有捐赠记录
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| doid  | int(10)     | NO   | PRI | NULL    | auto_increment |
| did   | int(10)     | NO   |     | NULL    |                |
| aname | varchar(65) | NO   |     |         |                |
| money | varchar(65) | YES  |     | NULL    |                |
| goods | varchar(65) | YES  |     | NULL    |                |
+-------+-------------+------+-----+---------+----------------+

    """
    doid = schema.Int(
            title=_(u"table primary key"),
        )
#     did = schema.Int(
#             title=_(u"juanzeng xiangmu id"),
#         )            
    did = schema.Choice(
            title=_(u"juanzeng xiangmu id"),
            vocabulary='xtcs.policy.vocabulary.donateId',
            required=True,
        )
    aname = schema.TextLine(
            title=_(u"juanzeng zhe"),
        )
    money = schema.Float(
            title=_(u"xianjin jin e"),            
            required=False
        )
    goods = schema.TextLine(
            title=_(u"juanzeng wuping"),
            required=False
        )            
    atime = schema.Datetime(
            title=_(u"juanzeng shi jian"),
            defaultFactory=nowDateTime
        )
    
    
class Donor(ORMBase):
    """Database-backed implementation of project
    """
    implements(IDonor)
    __tablename__ = 'donor'

    doid = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
    did = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )    

    aname = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    money = sqlalchemy.schema.Column(sqlalchemy.types.Float(13,2),
            nullable=False,
            default=""
        )
    goods = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    atime = sqlalchemy.schema.Column(sqlalchemy.types.DateTime(),
            nullable=True,
        )           

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
        
#所有有捐赠记录的项目,捐赠公示
class IDonate(Interface):
    """捐赠项目
    mysql> describe donate;
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| did        | int(10)      | NO   | PRI | NULL    | auto_increment |
| aname      | varchar(65)  | NO   |     | NULL    |                |
| amemo      | varchar(255) | YES  |     | null    |                |
| visible    | tinyint(1)   | NO   |     | 0       |                |
| start_time | int(10)      | NO   |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)
    
    """
    did = schema.Int(
            title=_(u"table primary key"),
        ) 
    start_time = schema.Datetime(
            title=_(u"kaishi shijian"),
            defaultFactory=nowDateTime            
        )           
    visible = schema.Int(
            title=_(u"shifou keshi?"),
            default=0
        )
    aname = schema.TextLine(
            title=_(u"cishan juanzeng xiangmu mingcheng"),
        )    
    amemo = schema.Text(
            title=_(u"cishan juanzeng xiangmu beizhu"),
        )


class Donate(ORMBase):
    """Database-backed implementation of project
    """
    implements(IDonate)
    __tablename__ = 'donate'

    did = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
    start_time = sqlalchemy.schema.Column(sqlalchemy.types.DateTime(),
            nullable=False,
        )
    visible = sqlalchemy.schema.Column(sqlalchemy.types.SmallInteger(),
            nullable=False,
        )
    aname = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    amemo = sqlalchemy.schema.Column(sqlalchemy.types.String(64),
            nullable=True,
        )