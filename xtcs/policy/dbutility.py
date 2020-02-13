#-*- coding: UTF-8 -*-
from xtcs.policy import Scope_session as Session
from xtcs.policy.ORMdbAPI import Dbapi
from xtcs.policy.mapping_db import OnlinePay
from xtcs.policy.mapping_db import AccessToken
from xtcs.policy.mapping_db import Donor
from xtcs.policy.mapping_db import Donate

#automap class start

onlinepay = Dbapi(Session,'xtcs.policy.mapping_db','onlinepay',OnlinePay)
accesstoken = Dbapi(Session,'xtcs.policy.mapping_db','accesstoken',AccessToken)
#automap end
search_clmns = ['aname']
donor = Dbapi(Session,'xtcs.policy.mapping_db','donor',Donor,fullsearch_clmns=search_clmns)
search_clmns = ['aname']
donate = Dbapi(Session,'xtcs.policy.mapping_db','donate',Donate,fullsearch_clmns=search_clmns)


    