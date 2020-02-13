  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
_ = MessageFactory('xtcs.policy')

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
import sys
reload(sys)
fmt = "%Y-%m-%d %H:%M:%S"
sys.setdefaultencoding('utf-8')
InputDb = "xtcs.policy:Input db"
ORMBase = declarative.declarative_base()
# linkstr = 'mysql://xtcs:XTcs82333685@404@127.0.0.1:3306/xtcs?charset=utf8'
linkstr = 'mysql+mysqldb://xtcs:XTcs82333685@404@127.0.0.1:3306/xtcs?charset=utf8'
# engine = create_engine('mysql://www.xtcs.org:XTcs82333685@404@127.0.0.1:3306/www.xtcs.org?charset=utf8', pool_recycle=3600)
engine = create_engine(linkstr,echo=False, pool_recycle=3600)
Scope_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine,expire_on_commit=False))
Session = Scope_session()

def maintan_session(session):
    "maintain sqlarchemy session"

    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()    