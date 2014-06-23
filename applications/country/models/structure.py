from sqlalchemy import or_, and_, create_engine, MetaData, Column, ForeignKey, func, \
    Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model, Ordered_DB_Model, auto_migrate
from ..configs.db import connection_string

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

class Country(DB_Model):
    __session__ = session
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "country_commodities" : ["country"],
            "country_enemies" : ["left_country"],
            "country_friends" : ["left_country"]
        }
    __detail_excluded_form_column__ = {
            "country_commodities" : ["country"],
            "country_enemies" : ["left_country"],
            "country_friends" : ["left_country"]
        }
    # Column's Labels
    __column_label__ = {
        "country_commodities" : "Commodities",
            "country_enemies" : "Enemies",
            "country_friends" : "Friends"
        }
    # Detail Column's Labels
    __detail_column_label__ = {
            "country_enemies" : {
                "right_country" : "Country"
            },
            "country_friends" : {
                "right_country" : "Country"
            }
        }
    # Fields Declarations
    name = Column(String(50))
    independence_date = Column(Date)
    rate = Column(Integer)
    developed = Column(Boolean)
    country_friends = relationship("Country_Friends", foreign_keys="Country_Friends.fk_left_country")
    friends = association_proxy("country_friends", "fk_right_country", creator=lambda _val: Country_Friends(right_country = _val))
    country_enemies = relationship("Country_Enemies", foreign_keys="Country_Enemies.fk_left_country")
    enemies = association_proxy("country_enemies", "fk_right_country", creator=lambda _val: Country_Enemies(right_country = _val))
    country_commodities = relationship("Country_Commodities", foreign_keys="Country_Commodities.fk_country")
    commodities = association_proxy("country_commodities", "fk_commodity", creator=lambda _val: Country_Commodities(commodity = _val))
    cities = relationship("City", foreign_keys="City.fk_country")
    fk_political_view = Column(Integer, ForeignKey("political_view._real_id"))
    political_view = relationship("Political_View", foreign_keys="Country.fk_political_view")
    
    

class Country_Friends(Ordered_DB_Model):
    __session__ = session
    # Fields Declarations
    fk_left_country = Column(Integer, ForeignKey("country._real_id"))
    fk_right_country = Column(Integer, ForeignKey("country._real_id"))
    left_country = relationship("Country", foreign_keys="Country_Friends.fk_left_country")
    right_country = relationship("Country", foreign_keys="Country_Friends.fk_right_country")
    
    def quick_preview(self):
        return self.right_country.quick_preview() + str(self._index)

class Country_Enemies(DB_Model):
    __session__ = session
    # Fields Declarations
    fk_left_country = Column(Integer, ForeignKey("country._real_id"))
    fk_right_country = Column(Integer, ForeignKey("country._real_id"))
    left_country = relationship("Country", foreign_keys="Country_Enemies.fk_left_country")
    right_country = relationship("Country", foreign_keys="Country_Enemies.fk_right_country")

class Commodity(DB_Model):
    __session__ = session
    # Fields Declarations
    name = Column(String(50))

class Country_Commodities(DB_Model):
    __session__ = session
    # Fields Declarations
    fk_country = Column(Integer, ForeignKey("country._real_id"))
    fk_commodity = Column(Integer, ForeignKey("commodity._real_id"))
    country = relationship("Country", foreign_keys="Country_Commodities.fk_country")
    commodity = relationship("Commodity", foreign_keys="Country_Commodities.fk_commodity")

class City(DB_Model):
    __session__ = session
    # Fields Declarations
    fk_country = Column(Integer, ForeignKey("country._real_id"))
    name = Column(String(50))

class Political_View(DB_Model):
    __session__ = session
    # Fields Declarations
    name = Column(String(50))


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on DB_Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)