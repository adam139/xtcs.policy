from dexterity.membrane.content.member import IOrganizationMember
from dexterity.membrane.behavior.membraneuser import INameFromFullName
from zope.component import adapter
from zope.interface import implementer

def get_full_name(context):
    if context.title != "":return context.title
    return u""

@implementer(INameFromFullName)
@adapter(IOrganizationMember)
class NameFromFullName(object):

    def __init__(self, context):
        self.context = context
    @property
    def title(self):
        return get_full_name(self.context)