from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, relationship, backref, association_proxy
from _config import session, metadata

DB_Model.metadata = metadata

class Theme(DB_Model):
    __session__          = session
    __id_prefix__        = 'Theme-'
    # Fields Declarations
    name                 = Column(String(50))
    content              = Column(Text)