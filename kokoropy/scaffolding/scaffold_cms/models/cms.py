from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, relationship, backref, association_proxy
from _config import session, metadata

DB_Model.metadata = metadata

class Cms(DB_Model):
    __session__ = session
    # Fields Declarations
    last_update          = Column(DateTime)
    version              = Column(String(50))

