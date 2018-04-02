# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone import api
from plone.app.dexterity.behaviors import constrains
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark
from logging import getLogger
logger = getLogger(__name__)

query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Document',
}]
defaultpath = {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/',
                }
gongyi_path = query.append(defaultpath.update({'v':'/cishanzixun/gongyixinwen'}))
huodong_path = query.append(defaultpath.update({'v':'/cishanzixun/huodongtonggao'}))
cishan_path = query.append(defaultpath.update({'v':'/cishanzixun/cishandongtai'})) 
STRUCTURE = [
    {
        'type': 'Folder',
        'title': u'慈善资讯',
        'id': 'cishanzixun',
        'description': u'慈善资讯',
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'Folder',
            'title': u'公益新闻',
            'id': 'gongyixinwen',
            'description': u'公益新闻',
            'layout': 'ajax_listings',
                      }, 
                     {
            'type': 'Folder',
            'title': u'活动通告',
            'id': 'huodongtonggao',
            'description': u'活动通告',
            'layout': 'ajax_listings',
                      }, 
                     {
            'type': 'Folder',
            'title': u'慈善动态',
            'id': 'cishandongtai',
            'description': u'慈善动态',
            'layout': 'ajax_listings',
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
            'description': u'图片新闻'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻2',
            'id': 'prdt2',
            'description': u'图片新闻2'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻3',
            'id': 'prdt3',
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
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'Folder',
            'title': u'推荐项目',
            'id': 'tuijianxiangmu',
            'description': u'推荐项目',
            'children': [
                         {
            'type': 'Project',
            'title': u'项目1',
            'id': 'xiangmu1',
            'description': u'项目1'
            },
              {'type': 'Project',
            'title': u'项目2',
            'id': 'xiangmu2',
            'description': u'项目2'
            },
            {'type': 'Project',
            'title': u'项目3',
            'id': 'xiangmu3',
            'description': u'项目3'
            },                         
                         
                         ]            
                      }                                                                         
                     ]
    },             
    {
        'type': 'Folder',
        'title': u'爱心捐赠',
        'id': 'aixinjuanzeng',
        'description': u'爱心捐赠',
        'layout': 'ajax_listings',
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
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'Folder',
            'title': u'捐赠公示',
            'id': 'juanzenggongshi',
            'description': u'捐赠公示',
            'markif':'xtcs.policy.interfaces.IJuanzenggongshi' 
                      }, 
                     {
            'type': 'Folder',
            'title': u'阳光屋',
            'id': 'yigongtuandui',
            'description': u'阳光屋',
            'layout': 'ajax_listings',
                      }                                                                         
                     ]
    },              
    {
        'type': 'Folder',
        'title': u'义工中心',
        'id': 'yigongzhongxin',
        'description': u'义工中心',
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'Folder',
            'title': u'义工活动',
            'id': 'yigonghuodong',
            'description': u'义工活动',
            'layout': 'ajax_listings',
                      }, 
                     {
            'type': 'Folder',
            'title': u'义工团队',
            'id': 'yigongtuandui',
            'description': u'义工团队',
            'layout': 'ajax_listings',
                      }                                                                         
                     ]
    },              
    {
        'type': 'Folder',
        'title': u'慈善社区',
        'id': 'cishanshequ',
        'description': u'慈善社区',
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'Folder',
            'title': u'慈善文摘',
            'id': 'cishanwenzhai',
            'description': u'慈善文摘',
            'layout': 'ajax_listings',
                      }, 
                     {
            'type': 'Folder',
            'title': u'爱心故事',
            'id': 'aixingushi',
            'description': u'爱心故事',
            'layout': 'ajax_listings',
                      }, 
                     {
            'type': 'Folder',
            'title': u'精彩博文',
            'id': 'jingcaibowen',
            'description': u'精彩博文',
            'layout': 'ajax_listings',
                      },
                     {
            'type': 'Folder',
            'title': u'论坛热帖',
            'id': 'luntanretie',
            'description': u'论坛热帖',
            'layout': 'ajax_listings',
                      }                                                                         
                     ]
    },             
    {
        'type': 'Folder',
        'title': u'组织管理',
        'id': 'zuzhiguanli',
        'description': u'组织管理',
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'Folder',
            'title': u'规章制度',
            'id': 'guizhangzhidu',
            'description': u'规章制度',
            'layout': 'ajax_listings',
                      }, 
                     {
            'type': 'Folder',
            'title': u'政策法规',
            'id': 'zhengcefagui',
            'description': u'政策法规',
            'layout': 'ajax_listings',
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
                     'query':gongyi_path,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'慈善动态',
                     'description': u'查询集',
                     'id':'cishan_path',
                     'query':cishan_path,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'活动通告',
                     'description': u'查询集',
                     'id':'huodongtonggao',
                     'query':huodong_path,
                     },
                    {
                     'type':'Collection',
                     'title':u'爱心故事',
                     'description': u'爱心故事',
                     'id':'aixingushi',
                     'query':gongyi_path,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'慈善文摘',
                     'description': u'慈善文摘',
                     'id':'cishanwenzhai',
                     'query':cishan_path,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'义工活动',
                     'description': u'义工活动',
                     'id':'yigonghuodong',
                     'query':huodong_path,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'政策法规',
                     'description': u'政策法规',
                     'id':'zhengcefagui',
                     'query':huodong_path,
                     }                                                                                     
                     ]
    },                           
    {
        'type': 'Folder',
        'title': u'帮助',
        'id': 'help',
        'description': u'帮助',
        'layout': 'ajax_listings',
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
       # give admin create memberarea
#     pm = api.portal.get_tool(name='portal_membership')
#     current = api.user.get_current()
#     try:
#         pm.memberareaCreationFlag = True
#         pm.createMemberarea(member_id= current.id)      
#         event.notify(MemberAreaCreatedEvent(current))
#     except:
#         return
    

    for item in STRUCTURE:
        _create_content(item, portal)
#     set relation

 
#     for i in range(1,20): 
#         user = api.user.create(
#                                username='test%s' % i,
# #                                fullname=u'张测%s',
#                                email='test%s@plone.org' % i,
#                                password='secret',
#                                )    
               
                


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
