#-*- coding: UTF-8 -*-
from xtcs.policy import Scope_session as Session
from xtcs.policy.ORMdbAPI import Dbapi
from xtcs.policy.mapping_db import AccessToken
from xtcs.policy.mapping_db import XiangMu
from xtcs.policy.mapping_db import JuanZeng


#automap class start
accesstoken = Dbapi(Session,'xtcs.policy.mapping_db','accesstoken',AccessToken)
xiangmu = Dbapi(Session,'xtcs.policy.mapping_db','xiangmu',XiangMu)
juanzeng = Dbapi(Session,'xtcs.policy.mapping_db','juanzeng',JuanZeng)
#automap end



    