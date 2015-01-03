from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option, Code,\
    relationship, backref, association_proxy, creator_maker, fk_column,\
    one_to_many, many_to_one, lookup_proxy
from _config import session, metadata

DB_Model.metadata = metadata

class Theme(DB_Model):
    __session__          = session
    __id_prefix__        = 'Theme-'
    # Fields Declarations
    name                 = Column(String(50))
    content              = Column(Code(language='css'))