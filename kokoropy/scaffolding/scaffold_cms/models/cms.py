from sqlalchemy import or_, and_, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model
from _config import session, metadata

DB_Model.metadata = metadata

class Cms(DB_Model):
    __session__ = session
    # Fields Declarations
    last_update          = Column(DateTime)
    version              = Column(String(50))

