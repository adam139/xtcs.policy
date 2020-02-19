#-*- coding: UTF-8 -*-
from xtcs.policy import Scope_session as Session
from xtcs.policy.ORMdbAPI import Dbapi
from xtcs.policy.mapping_db import AccessToken
from xtcs.policy.mapping_db import XiangMu
from xtcs.policy.mapping_db import JuanZeng


#automap class start
accesstoken = Dbapi(Session,'xtcs.policy.mapping_db','accesstoken',AccessToken)
search_clmns = ['mingcheng']
xiangmu = Dbapi(Session,'xtcs.policy.mapping_db','xiangmu',XiangMu,fullsearch_clmns=search_clmns)
search_clmns = ['xingming']
juanzeng = Dbapi(Session,'xtcs.policy.mapping_db','juanzeng',JuanZeng,fullsearch_clmns=search_clmns)
#automap end



    