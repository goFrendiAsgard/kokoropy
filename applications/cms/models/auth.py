from sqlalchemy import create_engine, MetaData, Column, ForeignKey, func, Integer, String,\
    Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model, auto_migrate
from ..configs.db import connection_string

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

class User(Model):
    __session__ = session
    # fields declaration
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    third_party_ids = relationship("Rel_User_Third_Party_Ids", foreign_keys="Rel_User_Third_Party_Ids.fk_left_user")
    groups = relationship("Rel_User_Groups", foreign_keys="Rel_User_Groups.fk_left_user")

class Third_Party(Model):
    __session__ = session
    # fields declaration


class Group(Model):
    __session__ = session
    # fields declaration

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

class Rel_User_Third_Party_Ids(Model):
    __session__ = session
    # fields declaration
    fk_left_user = Column(Integer, ForeignKey("user._real_id"))
    fk_right_third_party = Column(Integer, ForeignKey("third_party._real_id"))
    third_party = relationship("Third_Party", foreign_keys="Rel_User_Third_Party_Ids.fk_right_third_party")

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