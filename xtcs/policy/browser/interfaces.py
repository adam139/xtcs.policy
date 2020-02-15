from zope.interface import Interface
from zope import schema

from plone.theme.interfaces import IDefaultPloneLayer
from xtcs.policy import  _

class IwechatSettings(Interface):
    """Describes registry records
    """
    
    appid = schema.ASCII(
            title=_(u"app id"),
            description=_(u"weixin app id"),
        )
    appsecret = schema.ASCII(
                             title=_(u"app secret"),
                             description=_(u"weixin app secret"),
                             )
    token = schema.ASCII(
                             title=_(u"app token"),
                             description=_(u"weixin app token"),
                             )
    mchid = schema.ASCII(
                             title=_(u"shop id"),
                             description=_(u"shop id come from weixn"),
                             )
    key = schema.ASCII(
                             title=_(u"shop pay key"),
                             description=_(u"shop pay key"),
                             )
    notify_url = schema.ASCIILine(
            title=_(u"pay result notify url"),
            required=True,
        )
    curl_timeout = schema.Int(
            title=_(u"curl timeout"),
            required=True,
        )
    http_client = schema.ASCII(
            title=_(u"http client lib"),
            required=True,
        )                    
    access_token = schema.ASCII(
                             title=_(u"gongzhong hao access token"),
                             description=_(u"gongzhong hao access token"),
                             )
    access_token_time = schema.Datetime(
                             title=_(u"access token update time"),
                             description=_(u"gongzhong hao access token update time"),
                             )   
    jsapi_ticket = schema.ASCII(
                             title=_(u"jsapi ticket"),
                             description=_(u"jsapi web page authorized access ticket"),
                             )    
    jsapi_ticket_time = schema.Datetime(
                             title=_(u"jsapi ticket update time"),
                             description=_(u"jsapi access ticket update time"),
                             )                   
    preview = schema.ASCIILine(
            title=_(u"Preview image URL"),
            required=False,
        )
    hot_project = schema.Choice(
            title=_(u"tuijian xiangmu"),
            vocabulary='xtcs.policy.vocabulary.donateId',
            required=True,
        )   


class IThemeSpecific(Interface):
    """Marker interface that defines a ZTK browser layer. We can reference
    this in the 'layer' attribute of ZCML <browser:* /> directives to ensure
    the relevant registration only takes effect when this theme is installed.
    
    The browser layer is installed via the browserlayer.xml GenericSetup
    import step.
    """

class IDropdownConfiguration(Interface):
    """This interface defines the configlet for dropdown menus."""

    dropdown_depth = schema.Int(
        title=_(u"label_dropdown_depth", default=u'Depth of dropdown menus'),
        description=_(u"help_dropdown_depth",
                      default=u'How many levels to list after the top level.'),
        required=True,
        default=3)

    enable_caching = schema.Bool(
        title=_(u"label_enable_caching", default=u"Enable caching"),
        description=_(
            u"help_enable_caching",
            default=(u"WARNING! This is an experimental feature. "
                     u"This is using RAM to store cached template for "
                     u"dropdown menus. Technically every user and "
                     u"every visited section gets its own instance "
                     u"in the ram.cache. Don't enable this if you don't "
                     u"know what this is about. Disable this option "
                     u"if you get unexpected behavior of your global tabs.")),
        default=False,
        required=False)

    enable_parent_clickable = schema.Bool(
        title=_(u"label_enable_parent_clickable",
                default=u"Enable clicking menu items that have children"),
        description=_(
            u"help_enable_parent_clickable",
            default=(u"With this option enabled, every menu item is "
                     u"clickable. With this option disabled, an item is only "
                     u"clickable when it is not a parent so it has no "
                     u"children.")),
        default=True,
        required=False)


class IDropdownSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IDropdownMenuViewlet(Interface):
    """ Marker interface.
        Implements new functionality to global navigation that lets you to
        have dropdown menus for global navigation tabs. Dropdown menu is
        builded with navigation portlet's policy, so dropdowns contain items
        that are only allowed for navigation portlet. If the item is disabled
        for navigation portlet, it is disabled for dropdown menu automatically
    """

    def getTabObject(tabUrl=''):
        """Get the submenu tree for tab object"""
        
#set some mark interfaces for main nav folder container
class IProjectContainer(Interface):
    """
    This is really just a marker interface.
    mark the folder as project container.
    """           