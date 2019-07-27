# -*- coding: utf-8 -*-
from plone import api
from xtcs.policy.interfaces import IDonateLocator
from zope.component import getUtility
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def donateId(context):

    locator = getUtility(IDonateLocator)
    values = locator.query(start=0, size=100, multi=1, did=18, sortchildid=3)
    return SimpleVocabulary(
        [SimpleTerm(value=i.did, token=str(i.did), title=i.aname)
         for i in values],
    )
