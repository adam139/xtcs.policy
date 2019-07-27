# -*- coding: UTF-8 -*-
from plone.app.contenttypes.content import Document
from plone.app.contenttypes.interfaces import IDocument
from zope.interface import implementer


class IProject(IDocument):
    """
    xtcs project content type interface
    """


@implementer(IProject)
class Project(Document):
    """xtcs project content type
    """
