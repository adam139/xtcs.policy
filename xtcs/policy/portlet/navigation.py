
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.portlets.portlets.navigation import QueryBuilder
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class INonDefaultPageFilteringNavigationPortlet(INavigationPortlet):
    pass


class DontFilterDefaultQueryBuilder(QueryBuilder):
    implements(INavigationQueryBuilder)
    adapts(Interface, INonDefaultPageFilteringNavigationPortlet)

    def __init__(self, context, portlet):
        super(DontFilterDefaultQueryBuilder, self).__init__(context, portlet)
#        self.query['is_default_page'] = (True, False)  # Don't filter out default pages
#        import pdb
#        pdb.set_trace()
        self.query['sort_order'] = "reverse"
        self.query['sort_on'] = "created"
