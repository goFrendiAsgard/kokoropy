from sqlalchemy import or_, and_, create_engine, MetaData, Column, ForeignKey, func, \
    Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model, auto_migrate
from ..configs.db import connection_string
import hashlib

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

DB_Model.metadata = MetaData()

'''
    DB_Model has several commonly overriden property and methods:
    * __excluded_shown_column__       : list, hidden columns on "show detail" (e.g: ["id"])
    * __excluded_insert_column__      : list, hidden columns on "insert form" (e.g: ["id"])
    * __excluded_update_column__      : list, hidden columns on "edit form" (e.g: ["id"])
    * __prefix_of_id__                : string, prefix id (e.g: "%Y-")
    * __digit_num_of_id__             : integer, digit count after prefix id (e.g: 4)
'''
def encrypt_password(password):
    return hashlib.md5(hashlib.md5(password).hexdigest()).hexdigest()

class Cms(DB_Model):
    __session__ = session
    # fields declaration
    last_update = Column(DateTime)
    version = Column(String(50))

class Group(DB_Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    active = Column(Boolean)

class Third_Party_Authenticator(DB_Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    url = Column(String(255))
    callback_url = Column(String(255))
    active = Column(Boolean)

class Page(DB_Model):
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
    parent = relationship("Page", foreign_keys="Page.fk_page", uselist=False)
    fk_theme = Column(Integer, ForeignKey("theme._real_id"))
    theme = relationship("Theme", foreign_keys="Page.fk_theme")
    fk_layout = Column(Integer, ForeignKey("layout._real_id"))
    layout = relationship("Layout", foreign_keys="Page.fk_layout")
    active = Column(Boolean)
    
    def after_save(self):
        if self.page_order is None:
            query = self.session.query(func.max(Page.page_order).label("max_page_order")).filter(Page.fk_parent_id == self.fk_parent_id).one()
            max_page_order = query.max_page_order
            if max_page_order is None:
                max_page_order = 0
            self.page_order = max_page_order
    
    def build_input_static_content(self, **kwargs):
        value = self.static_content if self.static_content is not None else ''
        return '<textarea id="field_static_content" name="static_content" class="form-control" placeholder="Content">'+value+'</textarea>'

    def build_input_meta_description(self, **kwargs):
        value = self.meta_description if self.meta_description is not None else ''
        return '<textarea id="field_meta_description" name="meta_description" class="form-control" placeholder="Meta Description">'+value+'</textarea>'


class Page_Groups(DB_Model):
    __session__ = session
    # fields declaration
    fk_page = Column(Integer, ForeignKey("page._real_id"))
    fk_group = Column(Integer, ForeignKey("group._real_id"))
    page = relationship("Page", foreign_keys="Page_Groups.fk_page")
    group = relationship("Group", foreign_keys="Page_Groups.fk_group")

class Theme(DB_Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    content = Column(Text)
    custom_layout = relationship("Layout", foreign_keys="Layout.fk_theme")
    
    def build_input_content(self, **kwargs):
        value = self.content if self.content is not None else ''
        return '<textarea id="field_content" name="content" class="form-control" placeholder="Content">'+value+'</textarea>'


class Layout(DB_Model):
    __session__ = session
    # fields declaration
    fk_theme = Column(Integer, ForeignKey("theme._real_id"))
    name = Column(String(50))
    content = Column(Text)
    
    def build_input_content(self, **kwargs):
        value = self.content if self.content is not None else ''
        return '<textarea id="field_content" name="content" class="form-control" placeholder="Content">'+value+'</textarea>'

class Widget(DB_Model):
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
    
    def build_input_static_content(self, **kwargs):
        value = self.static_content if self.static_content is not None else ''
        return '<textarea id="field_static_content" name="static_content" class="form-control" placeholder="Content">'+value+'</textarea>'


class Widget_Groups(DB_Model):
    __session__ = session
    # fields declaration
    fk_widget = Column(Integer, ForeignKey("widget._real_id"))
    fk_group = Column(Integer, ForeignKey("group._real_id"))
    widget = relationship("Widget", foreign_keys="Widget_Groups.fk_widget")
    group = relationship("Group", foreign_keys="Widget_Groups.fk_group")

class User(DB_Model):
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
    
    @property
    def password(self):
        return None
    
    @password.setter
    def password(self, value):
        self.encrypted_password = encrypt_password(value)
    
    def assign_from_dict(self, variable):
        DB_Model.assign_from_dict(self, variable)
        if 'password' in variable and variable['password'] is not None and variable['password'] != '':
            self.password = variable['password']
    
    def build_custom_input(self, column_name, **kwargs):
        if column_name == 'password':
            return '<input id="field-password" name="password" placeholder="password">'
        else:
            return None

class User_Groups(DB_Model):
    __session__ = session
    # fields declaration
    fk_user = Column(Integer, ForeignKey("user._real_id"))
    fk_group = Column(Integer, ForeignKey("group._real_id"))
    user = relationship("User", foreign_keys="User_Groups.fk_user")
    group = relationship("Group", foreign_keys="User_Groups.fk_group")

class User_Third_Party_Identities(DB_Model):
    __session__ = session
    # fields declaration
    fk_user = Column(Integer, ForeignKey("user._real_id"))
    fk_third_party_authenticator = Column(Integer, ForeignKey("third_party_authenticator._real_id"))
    user = relationship("User", foreign_keys="User_Third_Party_Identities.fk_user")
    third_party_authenticator = relationship("Third_Party_Authenticator", foreign_keys="User_Third_Party_Identities.fk_third_party_authenticator")

class Language(DB_Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    iso_639_2 = Column(String(4))
    description = Column(Text)
    detail = relationship("Language_Detail", foreign_keys="Language_Detail.fk_language")
    
    def build_input_description(self, **kwargs):
        value = self.description if self.description is not None else ''
        return '<textarea id="field_description" name="description" class="form-control" placeholder="Language Description">'+value+'</textarea>'

class Language_Detail(DB_Model):
    __session__ = session
    # fields declaration
    fk_language = Column(Integer, ForeignKey("language._real_id"))
    word = Column(String(255))
    translation = Column(String(255))

class Configuration(DB_Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    value = Column(Text)
    
    def build_input_description(self, **kwargs):
        value = self.value if self.value is not None else ''
        return '<textarea id="field_value" name="value" class="form-control" placeholder="Configuration Value">'+value+'</textarea>'



'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on DB_Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)