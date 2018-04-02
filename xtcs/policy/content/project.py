#-*- coding: UTF-8 -*-
from zope.interface import implementer

from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.content import Document


class IProject(IDocument):
    """
    xtcs project content type interface
    """

@implementer(IProject)
class Project(Document):
    """xtcs project content type
    """