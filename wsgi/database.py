from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# OPENSHIFT_MYSQL_DB_HOST="127.6.27.1"
# OPENSHIFT_MYSQL_DB_LOG_DIR="/var/lib/openshift/d547df8d6cb84e10bc9c163994cac697//mysql-5.1/log"
# OPENSHIFT_MYSQL_DB_PASSWORD="6bbgzDwESXPL"
# OPENSHIFT_MYSQL_DB_PORT="3306"
# OPENSHIFT_MYSQL_DB_URL="mysql://admin:6bbgzDwESXPL@127.6.27.1:3306/"
# OPENSHIFT_MYSQL_DB_USERNAME="admin"
if 'OPENSHIFT_APP_UUID' in os.environ:
    # database_url = '%spython' % (os.environ['OPENSHIFT_MYSQL_DB_URL'])
    database_url = 'mysql://admin:m1Ua-Cg8MJqL@da531a6d91-joylin.rhcloud.com:47561/demo'
else:
    database_url = 'mysql://root@127.0.0.1/fwmrm_oltp_zfdang'
engine = create_engine(database_url, encoding='UTF-8', echo=True)


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
