from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option,\
    relationship, backref, association_proxy, creator_maker, fk_column,\
    one_to_many, many_to_one, lookup_proxy
from _config import session, metadata

DB_Model.metadata = metadata

class Language(DB_Model):
    __session__          = session
    __id_prefix__        = 'Lang-'
    # Fields Declarations
    name                 = Column(String(50))
    iso_639_2            = Column(String(4))
    description          = Column(Text)
    detail               = one_to_many("Language_Detail", "Language_Detail.fk_language")

class Language_Detail(DB_Model):
    __session__          = session
    __id_prefix__        = 'LDet-'
    # Fields Declarations
    fk_language          = fk_column("language._real_id")
    word                 = Column(String(255))
    translation          = Column(String(255))
