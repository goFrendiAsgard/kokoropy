from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model, auto_migrate
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

'''
    Model has several commonly overriden methods:
    * __unshowncolumn__          : list, hidden columns on "show detail" (e.g: ["id"])
    * __noninsertformcolumn__    : list, hidden columns on "insert form" (e.g: ["id"])
    * __nonupdateformcolumn__    : list, hidden columns on "edit form" (e.g: ["id"])
    * __prefixid__               : string, prefix id (e.g: "%Y-")
    * __digitid__                : integer, digit count after prefix id (e.g: 4)
'''

class Country(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))
    independence_date = Column(Date)
    rate = Column(Integer)
    developed = Column(Boolean)
    friends = relationship("Rel_Country_Friends", foreign_keys="Rel_Country_Friends.fk_left_country")
    enemies = relationship("Rel_Country_Enemies", foreign_keys="Rel_Country_Enemies.fk_left_country")
    commodities = relationship("Rel_Country_Commodities", foreign_keys="Rel_Country_Commodities.fk_left_country")
    cities = relationship("City", foreign_keys="City.fk_country")
    fk_political_view = Column(Integer, ForeignKey("political_view._real_id"))
    political_view = relationship("Political_View", foreign_keys="Country.fk_political_view")

class Rel_Country_Friends(Model):
    __session__ = session
    # fields declaration
    fk_left_country = Column(Integer, ForeignKey("country._real_id"))
    fk_right_country = Column(Integer, ForeignKey("country._real_id"))
    country = relationship("Country", foreign_keys="Rel_Country_Friends.fk_right_country")

class Rel_Country_Enemies(Model):
    __session__ = session
    # fields declaration
    fk_left_country = Column(Integer, ForeignKey("country._real_id"))
    fk_right_country = Column(Integer, ForeignKey("country._real_id"))
    country = relationship("Country", foreign_keys="Rel_Country_Enemies.fk_right_country")

class Commodity(Model):
    __session__ = session
    # fields declaration
    name = Column(String(50))

class Rel_Country_Commodities(Model):
    __session__ = session
    # fields declaration
    fk_left_country = Column(Integer, ForeignKey("country._real_id"))
    fk_right_commodity = Column(Integer, ForeignKey("commodity._real_id"))
    commodity = relationship("Commodity", foreign_keys="Rel_Country_Commodities.fk_right_commodity")

class City(Model):
    __session__ = session
    # fields declaration
    fk_country = Column(Integer, ForeignKey("country._real_id"))

class Political_View(Model):
    __session__ = session
    # fields declaration


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)