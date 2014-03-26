from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os.path import dirname
from os.path import join as path_join

# connection string
connection_string = 'sqlite:///' + path_join(dirname(dirname(__file__)), 'db', 'database.db')

# create engine
engine = create_engine(connection_string, echo=True)

# create db session
db_session = scoped_session(sessionmaker(bind=engine))