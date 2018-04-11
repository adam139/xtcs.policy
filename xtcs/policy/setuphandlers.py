# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone import api
from plone.app.dexterity.behaviors import constrains
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark

from plone.namedfile.file import NamedImage

from logging import getLogger
logger = getLogger(__name__)

# for image field data


data = open('/home/plone/workspace/Plone5sites/sites/src/xtcs.policy/xtcs/policy/tests/image.jpg','r').read()

image = NamedImage(data, 'image/jpg', u'image.jpg')

default = { 'i': 'portal_type',
           'o': 'plone.app.querystring.operation.string.is',
            'v': 'Document'}
query = []
defaultpath = {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/',
                }
import copy

defaultpath.update({'v':'/cishanzixun/gongyixinwen'})
gongyixinwen = [default,defaultpath]

cishandongtaipath = copy.copy(defaultpath)
cishandongtaipath.update({'v':'/cishanzixun/cishandongtai'})
cishandongtai = [default,cishandongtaipath]

huodongtonggaopath = copy.copy(defaultpath)
huodongtonggaopath.update({'v':'/cishanzixun/huodongtonggao'})
huodongtonggao = [default,huodongtonggaopath]

yigonghuodongpath = copy.copy(defaultpath)
yigonghuodongpath.update({'v':'/yigongzhongxin/yigonghuodong'})
yigonghuodong = [default,yigonghuodongpath] 

yigongtuanduipath = copy.copy(defaultpath)
yigongtuanduipath.update({'v':'/yigongzhongxin/yigongtuandui'})
yigongtuandui = [default,yigongtuanduipath]

cishanwenzhaipath = copy.copy(defaultpath)
cishanwenzhaipath.update({'v':'/cishanshequ/cishanwenzhai'})
cishanwenzhai = [default,cishanwenzhaipath]

aixingushipath = copy.copy(defaultpath)
aixingushipath.update({'v':'/cishanshequ/aixingushi'})
aixingushi = [default,aixingushipath]

jingcaibowenpath = copy.copy(defaultpath)
jingcaibowenpath.update({'v':'/cishanshequ/jingcaibowen'})
jingcaibowen = [default,jingcaibowenpath]

luntanretiepath = copy.copy(defaultpath)
luntanretiepath.update({'v':'/cishanshequ/luntanretie'})
luntanretie = [default,luntanretiepath]

guizhangzhidupath = copy.copy(defaultpath)
guizhangzhidupath.update({'v':'/zuzhiguanli/guizhangzhidu'})
guizhangzhidu = [default,guizhangzhidupath]

zhengcefaguipath = copy.copy(defaultpath)
zhengcefaguipath.update({'v':'/zuzhiguanli/zhengcefagui'})
zhengcefagui = [default,zhengcefaguipath]



STRUCTURE = [
    {
        'type': 'Folder',
        'title': u'慈善资讯',
        'id': 'cishanzixun',
        'description': u'慈善资讯',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'Folder',
            'title': u'公益新闻',
            'id': 'gongyixinwen',
            'description': u'公益新闻',
            'layout': 'tableview',
                      }, 
                     {
            'type': 'Folder',
            'title': u'活动通告',
            'id': 'huodongtonggao',
            'description': u'活动通告',
            'layout': 'tableview',
                      }, 
                     {
            'type': 'Folder',
            'title': u'慈善动态',
            'id': 'cishandongtai',
            'description': u'慈善动态',
            'layout': 'tableview',
                      },
                     {                                                                                     
            'type': 'my315ok.products.productfolder',
            'title': u'图片新闻',
            'id': 'tupianxinwen',
            'description': u'图片新闻',
            'children': [
                     {                                                                                     
            'type': 'my315ok.products.product',
            'title': u'图片新闻',
            'id': 'prdt1',
            'image':image,            
            'description': u'图片新闻'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻2',
            'id': 'prdt2',
            'image':image,            
            'description': u'图片新闻2'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻3',
            'id': 'prdt3',
            'image':image,            
            'description': u'图片新闻3'
                        }                                                                           
                         ]           
                      }
                     ]
    },
    {
        'type': 'Folder',
        'title': u'慈善项目',
        'id': 'cishanxiangmu',
        'description': u'慈善项目',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'my315ok.products.productfolder',
            'title': u'推荐项目',
            'id': 'tuijianxiangmu',
            'description': u'推荐项目'                      
                      }                                                                         
                     ]
    },             
    {
        'type': 'Folder',
        'title': u'爱心捐赠',
        'id': 'aixinjuanzeng',
        'description': u'爱心捐赠',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'Folder',
            'title': u'爱心捐款',
            'id': 'aixinjuankuan',
            'description': u'爱心捐款',
            'markif':'xtcs.policy.interfaces.IAixinjuankuan'            
                      }                                                                         
                     ]
    },             
    {
        'type': 'Folder',
        'title': u'爱心公示',
        'id': 'aixingongshi',
        'description': u'爱心公示',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'Folder',
            'title': u'捐赠公示',
            'id': 'juanzenggongshi',
            'description': u'捐赠公示',
            'layout':'donate_listings',
            'markif':'xtcs.policy.interfaces.IJuanzenggongshi' 
                      }, 
                     {
            'type': 'Folder',
            'title': u'阳光屋',
            'id': 'yigongtuandui',
            'description': u'阳光屋',
            'layout': 'tableview',
                      }                                                                         
                     ]
    },              
    {
        'type': 'Folder',
        'title': u'义工中心',
        'id': 'yigongzhongxin',
        'description': u'义工中心',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'Folder',
            'title': u'义工活动',
            'id': 'yigonghuodong',
            'description': u'义工活动',
            'layout': 'tableview',
                      }, 
                     {
            'type': 'Folder',
            'title': u'义工团队',
            'id': 'yigongtuandui',
            'description': u'义工团队',
            'layout': 'tableview',
                      }                                                                         
                     ]
    },              
    {
        'type': 'Folder',
        'title': u'慈善社区',
        'id': 'cishanshequ',
        'description': u'慈善社区',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'Folder',
            'title': u'慈善文摘',
            'id': 'cishanwenzhai',
            'description': u'慈善文摘',
            'layout': 'tableview',
                      }, 
                     {
            'type': 'Folder',
            'title': u'爱心故事',
            'id': 'aixingushi',
            'description': u'爱心故事',
            'layout': 'tableview',
                      }, 
                     {
            'type': 'Folder',
            'title': u'精彩博文',
            'id': 'jingcaibowen',
            'description': u'精彩博文',
            'layout': 'tableview',
                      },
                     {
            'type': 'Folder',
            'title': u'论坛热帖',
            'id': 'luntanretie',
            'description': u'论坛热帖',
            'layout': 'tableview',
                      }                                                                         
                     ]
    },             
    {
        'type': 'Folder',
        'title': u'组织管理',
        'id': 'zuzhiguanli',
        'description': u'组织管理',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'Folder',
            'title': u'规章制度',
            'id': 'guizhangzhidu',
            'description': u'规章制度',
            'layout': 'tableview',
                      }, 
                     {
            'type': 'Folder',
            'title': u'政策法规',
            'id': 'zhengcefagui',
            'description': u'政策法规',
            'layout': 'tableview',
                      }                                                                         
                     ]
    },
    {
        'type': 'Folder',
        'title': u'查询集',
        'id': 'sqls',
        'description': u'查询集',
        'children': [
                     {
                     'type':'Collection',
                     'title':u'公益新闻',
                     'description': u'查询集',
                     'id':'gongyixinwen',
                     'sort_on':'created',
                     'sort_reversed':True,
                     'query':gongyixinwen,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'慈善动态',
                     'description': u'查询集',
                     'id':'cishandongtai',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':cishandongtai,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'活动通告',
                     'description': u'活动通告',
                     'id':'huodongtonggao',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':huodongtonggao,
                     },
                    {
                     'type':'Collection',
                     'title':u'慈善文摘',
                     'description': u'慈善文摘',
                     'id':'cishanwenzhai',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':cishanwenzhai,
                     },                     
                    {
                     'type':'Collection',
                     'title':u'爱心故事',
                     'description': u'爱心故事',
                     'id':'aixingushi',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':aixingushi,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'精彩博文',
                     'description': u'精彩博文',
                     'id':'jingcaibowen',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':jingcaibowen,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'论坛热帖',
                     'description': u'论坛热帖',
                     'id':'luntanretie',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':luntanretie,
                     },                     
                     {                     
                     'type':'Collection',
                     'title':u'义工活动',
                     'description': u'义工活动',
                     'id':'yigonghuodong',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':yigonghuodong,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'义工团队',
                     'description': u'义工团队',
                     'id':'yigongtuandui',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':yigongtuandui,
                     },                     
                     {                     
                     'type':'Collection',
                     'title':u'政策法规',
                     'description': u'政策法规',
                     'id':'zhengcefagui',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':zhengcefagui,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'规章制度',
                     'description': u'规章制度',
                     'id':'guizhangzhidu',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':guizhangzhidu,
                     }                                                                                                          
                     ]
    },                           
    {
        'type': 'Folder',
        'title': u'帮助',
        'id': 'help',
        'description': u'帮助',
        'layout': 'tableview',
    }
               
]


def isNotCurrentProfile(context):
    return context.readDataFile('policy_marker.txt') is None


def post_install(context):
    """Setuphandler for the profile 'default'
    """
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package
#     return
    portal = api.portal.get()
#     members = portal.get('events', None)
#     if members is not None:
#         api.content.delete(members)
    members = portal.get('news', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('Members', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
  

    for item in STRUCTURE:
        _create_content(item, portal)
#     set relation


def content(context):
    """Setuphandler for the profile 'content'
    """
    if context.readDataFile('policy_content_marker.txt') is None:
        return
    pass



def _create_content(item, container):
    new = container.get(item['id'], None)
    if not new:

        new = api.content.create(
            type=item['type'],
            container=container,
            title=item['title'],
            description=item['description'],            
            id=item['id'],
            safe_id=False)
        logger.info('Created item {}'.format(new.absolute_url()))
    
    if item.get('layout', False):
        new.setLayout(item['layout'])
    if item.get('query', False):
        new.query = item['query']
    if item.get('sort_on', False):
        new.sort_on = item['sort_on']
    if item.get('sort_reversed', False):
        new.sort_reversed = item['sort_reversed']                
    if item.get('image', False):
        new.image = item['image']               
    if item.get('markif', False):
        try:
            ifobj = resolve(item['markif'])
            mark(new,ifobj)
        except:
            pass                
    if item.get('default-page', False):
        new.setDefaultPage(item['default-page'])
    if item.get('allowed_types', False):
        _constrain(new, item['allowed_types'])
    if item.get('local_roles', False):
        for local_role in item['local_roles']:
            api.group.grant_roles(
                groupname=local_role['group'],
                roles=local_role['roles'],
                obj=new)
    if item.get('publish', False):
        api.content.transition(new, to_state=item.get('state', 'published'))
    new.reindexObject()
    # call recursively for children
    for subitem in item.get('children', []):
        _create_content(subitem, new)


def _constrain(context, allowed_types):
    behavior = ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)
