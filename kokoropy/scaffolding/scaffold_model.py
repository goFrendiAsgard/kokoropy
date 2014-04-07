from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from kokoropy.model import Mixin
from ..configs.db import connection_string

# create Base
Base = declarative_base()
engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

class G_Table_Name(Base, Mixin):
    __tablename__ = 'g_table_name'
    __session__ = session
    # g_column

Base.metadata.create_all(bind=engine)