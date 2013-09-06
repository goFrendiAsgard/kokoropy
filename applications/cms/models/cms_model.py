import os
from kokoropy.sqlalchemy import create_engine, ForeignKey
from kokoropy.sqlalchemy import Column, Date, Integer, String, Boolean
from kokoropy.sqlalchemy.ext.declarative import declarative_base
from kokoropy.sqlalchemy.orm import relationship, backref, sessionmaker

db_location = os.path.join(os.path.abspath('db'),'cms.db')
print db_location
connection_string = 'sqlite:///'+db_location
 
engine = create_engine(connection_string, echo=True)
Base = declarative_base()

def encrypt_password(password):
    import md5
    return md5.md5(password).hexdigest()

####################################################################################
# Groups Table
class Group(Base):
    
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
    

####################################################################################
# Users Table
class User(Base):
    
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    encrypted_password = Column(String)
    real_name = Column(String)
    email = Column(String)
    
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
class Page(Base):
    
    __tablename__ = 'pages'
    page_id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    is_static = Column(Boolean)
    content = Column(String)
    url = Column(String)
    privilege = Column(Integer)
    
    def __init__(self, name, title, is_static=1, content='', url='', privilege=0):
        self.name = name
        self.title = title
        self.is_static = is_static
        self.content = content
        self.url = url
        self.privilege = privilege
    
    
####################################################################################
# Widgets Table
class Widget(Base):
    
    __tablename__ = 'widgets'
    widget_id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    is_static = Column(Boolean)
    content = Column(String)
    url = Column(String)
    privilege = Column(Integer)
    
    def __init__(self, name, title, is_static=1, content='', url='', privilege=0):
        self.name = name
        self.title = title
        self.is_static = is_static
        self.content = content
        self.url = url
        self.privilege = privilege
        
class User_Group(Base):
    
    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    group_id = Column(Integer)
    #user = relationship(User, backref='groups', primaryjoin=(user_id==User.user_id))
    #group = relationship(Group, backref='users', primaryjoin=(group_id==Group.group_id))

####################################################################################
# CMS Model
####################################################################################
class CMS_Model(object):
    
    def __init__(self):
        pass
    
    def build_database(self):
        Base.metadata.create_all(engine)
    
if __name__ == '__main__':
    model = CMS_Model()
    model.build_database()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    group = Group(name="admin")
    user = User(user_name="Tono", password="mboh", real_name="Tono Martono")
    
    session.add(user)
    session.commit()