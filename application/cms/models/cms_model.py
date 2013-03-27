from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///cms.db', echo=True)
Base = declarative_base()

class Groups(Base):
    __tablename__ = 'groups'
    group_id = Column('group_id', Integer, primary_key=True)
    name = Column('name', String)
    pass

class Users(Base):
    __tablename__ = 'users'
    user_id = Column('user_id', Integer, primary_key=True)
    user_name = Column('name', String)
    password = Column('password', String)
    pass

class Pages(Base):
    __tablename__ = 'pages'
    page_id = Column('page_id', Integer, primary_key=True)
    name = Column('name', String)
    pass

class Widgets(Base):
    __tablename__ = 'widgets'
    page_id = Column('widget_id', Integer, primary_key=True)
    name = Column('name', String)
    pass

class CMS_Model(object):
    def __init__(self):
        pass