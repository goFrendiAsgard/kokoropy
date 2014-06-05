from sqlalchemy import or_, and_, create_engine, MetaData, Column, ForeignKey, func, \
    Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import Model, auto_migrate
from kokoropy import request
from ..configs.db import connection_string
import hashlib, re, getpass

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

Model.metadata = MetaData()

'''
    Model has several commonly overriden property and methods:
    * __excluded_shown_column__       : list, hidden columns on "show detail" (e.g: ["id"])
    * __excluded_insert_column__      : list, hidden columns on "insert form" (e.g: ["id"])
    * __excluded_update_column__      : list, hidden columns on "edit form" (e.g: ["id"])
    * __prefix_of_id__                : string, prefix id (e.g: "%Y-")
    * __digit_num_of_id__             : integer, digit count after prefix id (e.g: 4)
'''

class Cms(Model):
    __session__ = session
    # fields declaration
    last_update = Column(DateTime)
    version = Column(String(50))

class Group(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    active = Column(Boolean)
    
    def quick_preview(self):
        return self.name

class Third_Party_Authenticator(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    url = Column(String(255))
    callback_url = Column(String(255))
    active = Column(Boolean)
    
    def quick_preview(self):
        return self.name

class Page(Model):
    __session__ = session
    __detail_excluded_shown_column__ = {
            "page_groups" : ["page"]
        }
    __detail_excluded_form_column__ = {
            "page_groups" : ["page"]
        }
    # fields declaration
    name = Column(String(50))
    title = Column(String(255))
    meta_author = Column(String(255))
    meta_keyword = Column(Text)
    meta_description = Column(Text)
    static = Column(Boolean)
    url = Column(String(255))
    static_content = Column(Text)
    authorization = Column(Integer)
    page_order = Column(Integer)
    page_groups = relationship("Page_Groups", foreign_keys="Page_Groups.fk_page")
    groups = association_proxy("page_groups", "fk_group", creator=lambda _val: Page_Groups(group = _val))
    fk_page = Column(Integer, ForeignKey("page._real_id"))
    parent = relationship("Page", foreign_keys="Page.fk_page")
    fk_theme = Column(Integer, ForeignKey("theme._real_id"))
    theme = relationship("Theme", foreign_keys="Page.fk_theme")
    fk_layout = Column(Integer, ForeignKey("layout._real_id"))
    layout = relationship("Layout", foreign_keys="Page.fk_layout")
    active = Column(Boolean)
    
    def quick_preview(self):
        return self.name
    
    def after_save(self):
        if self.page_order is None:
            query = self.session.query(func.max(Page.page_order).label("max_page_order")).filter(Page.fk_parent_id == self.fk_parent_id).one()
            max_page_order = query.max_page_order
            if max_page_order is None:
                max_page_order = 0
            self.page_order = max_page_order

class Page_Groups(Model):
    __session__ = session
    # fields declaration
    fk_page = Column(Integer, ForeignKey("page._real_id"))
    fk_group = Column(Integer, ForeignKey("group._real_id"))
    page = relationship("Page", foreign_keys="Page_Groups.fk_page")
    group = relationship("Group", foreign_keys="Page_Groups.fk_group")

class Theme(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    content = Column(Text)
    custom_layout = relationship("Layout", foreign_keys="Layout.fk_theme")
    
    def quick_preview(self):
        return self.name

class Layout(Model):
    __session__ = session
    # fields declaration
    fk_theme = Column(Integer, ForeignKey("theme._real_id"))
    name = Column(String(50))
    content = Column(Text)
    
    def quick_preview(self):
        return self.name

class Widget(Model):
    __session__ = session
    __detail_excluded_shown_column__ = {
            "widget_groups" : ["widget"]
        }
    __detail_excluded_form_column__ = {
            "widget_groups" : ["widget"]
        }
    # fields declaration
    name = Column(String(50))
    static = Column(Boolean)
    url = Column(String(255))
    static_content = Column(Text)
    authorization = Column(Integer)
    widget_groups = relationship("Widget_Groups", foreign_keys="Widget_Groups.fk_widget")
    groups = association_proxy("widget_groups", "fk_group", creator=lambda _val: Widget_Groups(group = _val))
    active = Column(Boolean)
    
    def quick_preview(self):
        return self.name

class Widget_Groups(Model):
    __session__ = session
    # fields declaration
    fk_widget = Column(Integer, ForeignKey("widget._real_id"))
    fk_group = Column(Integer, ForeignKey("group._real_id"))
    widget = relationship("Widget", foreign_keys="Widget_Groups.fk_widget")
    group = relationship("Group", foreign_keys="Widget_Groups.fk_group")

class User(Model):
    __session__ = session
    __detail_excluded_shown_column__ = {
            "user_third_party_identities" : ["user"],
            "user_groups" : ["user"]
        }
    __detail_excluded_form_column__ = {
            "user_third_party_identities" : ["user"],
            "user_groups" : ["user"]
        }
    # fields declaration
    username = Column(String(255))
    realname = Column(String(255))
    email = Column(String(255))
    photo = Column(String(255))
    encrypted_password = Column(String(255))
    user_groups = relationship("User_Groups", foreign_keys="User_Groups.fk_user")
    groups = association_proxy("user_groups", "fk_group", creator=lambda _val: User_Groups(group = _val))
    user_third_party_identities = relationship("User_Third_Party_Identities", foreign_keys="User_Third_Party_Identities.fk_user")
    third_party_identities = association_proxy("user_third_party_identities", "fk_third_party_authenticator", creator=lambda _val: User_Third_Party_Identities(third_party_authenticator = _val))
    last_login = Column(DateTime)
    active = Column(Boolean)
    fk_language = Column(Integer, ForeignKey("language._real_id"))
    language = relationship("Language", foreign_keys="User.fk_language")
    
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

class User_Groups(Model):
    __session__ = session
    # fields declaration
    fk_user = Column(Integer, ForeignKey("user._real_id"))
    fk_group = Column(Integer, ForeignKey("group._real_id"))
    user = relationship("User", foreign_keys="User_Groups.fk_user")
    group = relationship("Group", foreign_keys="User_Groups.fk_group")

class User_Third_Party_Identities(Model):
    __session__ = session
    # fields declaration
    fk_user = Column(Integer, ForeignKey("user._real_id"))
    fk_third_party_authenticator = Column(Integer, ForeignKey("third_party_authenticator._real_id"))
    user = relationship("User", foreign_keys="User_Third_Party_Identities.fk_user")
    third_party_authenticator = relationship("Third_Party_Authenticator", foreign_keys="User_Third_Party_Identities.fk_third_party_authenticator")

class Language(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    iso_639_2 = Column(String(4))
    description = Column(Text)
    detail = relationship("Language_Detail", foreign_keys="Language_Detail.fk_language")
    
    def quick_preview(self):
        return self.name

class Language_Detail(Model):
    __session__ = session
    # fields declaration
    fk_language = Column(Integer, ForeignKey("language._real_id"))
    word = Column(String(255))
    translation = Column(String(255))
    
    def quick_preview(self):
        return self.word

class Configuration(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    value = Column(Text)
    
    def quick_preview(self):
        return self.name

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
        super_user.groups.append(super_admin)
        super_user.save()


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)