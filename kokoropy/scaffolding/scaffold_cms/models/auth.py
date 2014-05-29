from sqlalchemy import or_, and_, create_engine, MetaData, Column, ForeignKey, func, Integer, String,\
    Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import Model, auto_migrate
from kokoropy import request
from ..configs.db import connection_string
import hashlib
import getpass
import re

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

def do_login(identity, password):
    user_list = User.get(and_(or_(User.username == identity, User.email == identity), User.encrypted_password == encrypt_password(password)))
    if len(user_list) > 0:
        user = user_list[0]
        request.SESSION['__user_id'] = user.id
        return True
    else:
        return False

def do_logout():
    if '__user_id' in request.SESSION:
        request.SESSION.remove('__user_id')

def get_current_user():
    if '__user_id' in request.SESSION:
        user_id = request.SESSION['__user_id']
        user = User.find(user_id)
        return user

class User(Model):
    __session__ = session
    __excluded_shown_column__ = ['id', 'encrypted_password']
    __form_column__ = ['username', 'realname', 'email', 'password', 'groups']
    # fields declaration
    username = Column(String(255), unique=True)
    realname = Column(String(255))
    email = Column(String(255), unique=True)
    encrypted_password = Column(String(255))
    third_party_ids = relationship("Third_Party_Id", foreign_keys="Third_Party_Id.fk_left_user")
    usergroups = relationship("Rel_User_Groups", foreign_keys="Rel_User_Groups.fk_left_user")
    groups = association_proxy("usergroups", "group", creator=lambda _i: Rel_User_Groups(group=_i))
    
    def quick_preview(self):
        return self.username
    
    @property
    def password(self):
        return None
    
    @password.setter
    def password(self, value):
        self.encrypted_password = encrypt_password(value)
    
    def assign_from_dict(self, variable):
        Model.assign_from_dict(self, variable)
        if 'password' in variable and variable['password'] is not None and variable['password'] != '':
            self.password = variable['password']
    
    def build_custom_input(self, column_name, **kwargs):
        if column_name == 'password':
            return '<input id="field-password" name="password" placeholder="password">'
        else:
            return None

class Third_Party(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    url = Column(String(255))
    callback_url = Column(String(255))
    
    def quick_preview(self):
        return self.name


class Group(Model):
    __session__ = session
    __excluded_shown_column__ = ['id']
    __excluded_form_column__ = ['id']
    # fields declaration
    name = Column(String(255))
    
    def quick_preview(self):
        return self.name

class Page(Model):
    __session__ = session
    __excluded_shown_column__ = ['id', 'page_order']
    __excluded_form_column__ = ['id', 'page_order', 'children']
    __tabular_form_column__ = ['name', 'title', 'url', 'authorization', 'groups']
    __tabular_shown_column__ = ['name', 'title', 'url', 'authorization', 'groups']
    # fields declaration
    name = Column(String(50))
    url = Column(String(50))
    title = Column(String(50))
    meta_author = Column(String(255))
    meta_keyword = Column(String(255))
    meta_description = Column(String(255))
    static = Column(Boolean)
    static_content = Column(Text)
    authorization = Column(Integer)
    groups = relationship("Rel_Page_Groups", foreign_keys="Rel_Page_Groups.fk_left_page")
    fk_parent_id = Column(Integer, ForeignKey('page._real_id'))
    children = relationship("Page", foreign_keys="Page.fk_parent_id")
    page_order = Column(Integer)
    
    def quick_preview(self):
        return self.name
    
    def after_save(self):
        if self.page_order is None:
            query = self.session.query(func.max(Page.page_order).label("max_page_order")).filter(Page.fk_parent_id == self.fk_parent_id).one()
            max_page_order = query.max_page_order
            if max_page_order is None:
                max_page_order = 0
            self.page_order = max_page_order

class Third_Party_Id(Model):
    __session__ = session
    __excluded_shown_column__ = ['id']
    # fields declaration
    fk_left_user = Column(Integer, ForeignKey("user._real_id"))
    fk_right_third_party = Column(Integer, ForeignKey("third_party._real_id"))
    third_party = relationship("Third_Party", foreign_keys="Third_Party_Id.fk_right_third_party")
    code = Column(String(50))

class Rel_User_Groups(Model):
    __session__ = session
    __excluded_shown_column__ = ['id']
    # fields declaration
    fk_left_user = Column(Integer, ForeignKey("user._real_id"))
    fk_right_group = Column(Integer, ForeignKey("group._real_id"))
    group = relationship("Group", foreign_keys="Rel_User_Groups.fk_right_group")
    user = relationship("User", foreign_keys="Rel_User_Groups.fk_left_user")

class Rel_Page_Groups(Model):
    __session__ = session
    __excluded_shown_column__ = ['id']
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
    else:
        super_admin = Group.get()[0]
    
    if User.count() == 0:
        print('No user registered to this system. Please add a new one !!!')
        username = raw_input('New user name : ')
        realname = raw_input('Real name : ')
        email = ''
        password = ''
        confirm_password = ''
        while True:
            email = raw_input('Email : ')
            if re.match(r'[^@]+@[^@]+\.[^@]+', email):
                break
            else:
                print('Invalid email address, please insert again')
        while True:
            password = getpass.getpass('Password : ')
            confirm_password = getpass.getpass('Password (again) :')
            if password == confirm_password:
                break
            else:
                print('Password doesn\'t match, please insert again')
        super_user = User()
        super_user.username = username
        super_user.realname = realname
        super_user.email = email
        super_user.password = password
        #rel_user_group = Rel_User_Groups()
        #rel_user_group.group = super_admin
        #super_user.groups.append(rel_user_group)
        super_user.groups.append(super_admin)
        super_user.save()
insert_default()