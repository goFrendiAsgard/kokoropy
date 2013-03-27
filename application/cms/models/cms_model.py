from kokoropy.sqlalchemy import create_engine, ForeignKey
from kokoropy.sqlalchemy import Column, Date, Integer, String
from kokoropy.sqlalchemy.ext.declarative import declarative_base
from kokoropy.sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///cms.db', echo=True)
Base = declarative_base()

def encrypt_password(password):
    import md5
    return md5.md5(password).hexdigest()

####################################################################################
# Groups Table
class Groups(Base):
    
    __tablename__ = 'groups'
    group_id = Column('group_id', Integer, primary_key=True)
    name = Column('name', String)
    
    def __init__(self, name):
        self.name = name
    

####################################################################################
# Users Table
class Users(Base):
    
    __tablename__ = 'users'
    user_id = Column('user_id', Integer, primary_key=True)
    user_name = Column('name', String)
    encrypted_password = Column('encrypted_password', String)
    real_name = Column('real_name', String)
    email = Column('email', String)
    
    def __init__(self, user_name, password="", real_name="", email=""):
        self.user_name = user_name
        self.encrypted_password = encrypt_password(password)
        self.real_name = real_name
        self.email = email
    
    def is_match(self, user_name, password):
        return (user_name == self.user_name or user_name == self.email) and \
            encrypt_password(password) == self.encrypted_password
    

####################################################################################
# Pages Table
class Pages(Base):
    
    __tablename__ = 'pages'
    page_id = Column('page_id', Integer, primary_key=True)
    name = Column('name', String)
    title = Column('name', String)
    privilege = Column('privilege', Integer)
    
    
####################################################################################
# Widgets Table
class Widgets(Base):
    
    __tablename__ = 'widgets'
    page_id = Column('widget_id', Integer, primary_key=True)
    name = Column('name', String)
    

####################################################################################
# Widgets Table
####################################################################################
class CMS_Model(object):
    
    def __init__(self):
        pass