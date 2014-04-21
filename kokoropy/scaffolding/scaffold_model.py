from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model, auto_migrate
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

# g_structure
'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)