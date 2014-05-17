from sqlalchemy import create_engine, MetaData, Column, ForeignKey, func, Integer, String,\
    Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model, auto_migrate
from ..configs.db import connection_string
import hashlib

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

Model.metadata = MetaData()

'''
    Model has several commonly overriden methods:
    * __unshowncolumn__          : list, hidden columns on "show detail" (e.g: ["id"])
    * __noninsertformcolumn__    : list, hidden columns on "insert form" (e.g: ["id"])
    * __nonupdateformcolumn__    : list, hidden columns on "edit form" (e.g: ["id"])
    * __prefixid__               : string, prefix id (e.g: "%Y-")
    * __digitid__                : integer, digit count after prefix id (e.g: 4)
'''

def encrypt_password(password):
    return hashlib.md5(hashlib.md5(password).hexdigest()).hexdigest()

class User(Model):
    __session__ = session
    __unshowncolumn__ = ['id', 'encrypted_password']
    __nonformcolumn__ = ['id', 'encrypted_password']
    # fields declaration
    username = Column(String(255), unique=True)
    realname = Column(String(255))
    email = Column(String(255), unique=True)
    encrypted_password = Column(String(255))
    third_party_ids = relationship("Rel_User_Third_Party_Ids", foreign_keys="Rel_User_Third_Party_Ids.fk_left_user")
    groups = relationship("Rel_User_Groups", foreign_keys="Rel_User_Groups.fk_left_user")
    
    def quick_preview(self):
        return self.username
    
    @property
    def password(self):
        return None
    
    @password.setter
    def password(self, value):
        self.encrypted_password = encrypt_password(value)
    
    def login(self, identity, password):
        pass

class Third_Party(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    url = Column(String(255))
    
    def quick_preview(self):
        return self.name


class Group(Model):
    __session__ = session
    # fields declaration
    name = Column(String(255))
    
    def quick_preview(self):
        return self.name

class Page(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    url = Column(String(50))
    title = Column(String(50))
    meta_keyword = Column(String(255))
    meta_description = Column(String(255))
    static = Column(Boolean)
    static_content = Column(Text)
    authorization = Column(Integer)
    groups = relationship("Rel_Page_Groups", foreign_keys="Rel_Page_Groups.fk_left_page")
    
    def quick_preview(self):
        return self.name

class Rel_User_Third_Party_Ids(Model):
    __session__ = session
    # fields declaration
    fk_left_user = Column(Integer, ForeignKey("user._real_id"))
    fk_right_third_party = Column(Integer, ForeignKey("third_party._real_id"))
    third_party = relationship("Third_Party", foreign_keys="Rel_User_Third_Party_Ids.fk_right_third_party")
    code = Column(String(50))

class Rel_User_Groups(Model):
    __session__ = session
    # fields declaration
    fk_left_user = Column(Integer, ForeignKey("user._real_id"))
    fk_right_group = Column(Integer, ForeignKey("group._real_id"))
    group = relationship("Group", foreign_keys="Rel_User_Groups.fk_right_group")

class Rel_Page_Groups(Model):
    __session__ = session
    # fields declaration
    fk_left_page = Column(Integer, ForeignKey("page._real_id"))
    fk_right_group = Column(Integer, ForeignKey("group._real_id"))
    group = relationship("Group", foreign_keys="Rel_Page_Groups.fk_right_group")


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)

def insert_default():
    # default action
    if Group.count() == 0:
        super_admin = Group()
        super_admin.name = 'Super Admin'
        super_admin.save()
        #session.add(super_admin)
        #session.commit()
    else:
        super_admin = Group.get()[0]
    
    if User.count() == 0:
        print('No user registered to this system. Please add a new one !!!')
        username = raw_input('New user name : ')
        realname = raw_input('Real name : ')
        email = raw_input('Email : ')
        password = raw_input('Password : ')
        confirm_password = raw_input('Password (again) : ')
        while password != confirm_password:
            print('Password doesn\'t match, please insert again')
            password = raw_input('Password : ')
            confirm_password = raw_input('Password (again ) :')
        super_user = User()
        super_user.username = username
        super_user.realname = realname
        super_user.email = email
        super_user.password = password
        rel_user_group = Rel_User_Groups()
        rel_user_group.group = super_admin
        super_user.groups.append(rel_user_group)
        super_user.save()
        #session.add(super_user)
        #session.commit()
        #print 'jumlah user ', User.count()
        #print super_user.groups[0].name
        #print ('is it?', super_admin in super_user.groups)
insert_default()