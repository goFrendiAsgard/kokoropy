from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, relationship, backref, association_proxy
from _config import session, metadata

DB_Model.metadata = metadata

class Language(DB_Model):
    __session__          = session
    __id_prefix__        = 'Lang-'
    # Fields Declarations
    name                 = Column(String(50))
    iso_639_2            = Column(String(4))
    description          = Column(Text)
    detail               = relationship("Language_Detail", foreign_keys="Language_Detail.fk_language")

class Language_Detail(DB_Model):
    __session__          = session
    __id_prefix__        = 'LDet-'
    # Fields Declarations
    fk_language          = Column(Integer, ForeignKey("language._real_id"))
    word                 = Column(String(255))
    translation          = Column(String(255))
