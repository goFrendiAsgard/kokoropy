from kokoropy.model import DB_Model, Ordered_DB_Model, or_, and_, Column, ForeignKey, func, relationship,\
    backref, association_proxy, creator_maker, fk_column, one_to_many, many_to_one, lookup_proxy,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option, RichText, Code
from _config import session, metadata

DB_Model.metadata = metadata

class Structure(Ordered_DB_Model):
    __session__          = session
    # Fields Declarations
    fk_village           = fk_column("village._real_id")
    name                 = Column(String(50))

