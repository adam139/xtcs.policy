  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
_ = MessageFactory('xtcs.policy')

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
InputDb = "xtcs.policy:Input db"
ORMBase = declarative.declarative_base()
engine = create_engine('mysql://www.xtcs.org:XTcs82333685@404@127.0.0.1:3306/www.xtcs.org?charset=utf8', pool_recycle=3600)
Session = sessionmaker(bind=engine)
Session = Session()