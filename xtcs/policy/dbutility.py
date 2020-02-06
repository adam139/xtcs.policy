#-*- coding: UTF-8 -*-
from xtcs.policy import Scope_session as Session
from xtcs.policy.ORMdbAPI import Dbapi
from xtcs.policy.mapping_db import OnlinePay

#automap class start
search_clmns = ['openid']
onlinepay = Dbapi(Session,'xtcs.policy.mapping_db','onlinepay',OnlinePay,fullsearch_clmns=search_clmns)


    