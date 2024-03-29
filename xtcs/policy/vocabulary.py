# -*- coding: utf-8 -*-
from zope.interface import provider
# from xtcs.policy.interfaces import IDbapi
from sqlalchemy.dbapi.interfaces import IDbapi
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import queryUtility


@provider(IVocabularyFactory)
def donateId(context):

    locator = queryUtility(IDbapi, name='xiangmu')
#     values = locator.query(start=0,size=100,multi=1,did=18,sortchildid=3)
    args = {"start":0,"size":10,'SearchableText':'',
                'with_entities':0,'sort_order':'reverse'}
    values = locator.query(args) 
    return SimpleVocabulary(
        [SimpleTerm(value=int(i.id), token=str(i.id), title=i.mingcheng) for i in values],
    )
