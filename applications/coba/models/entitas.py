from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

class Child(Model):
    __session__ = session
    _entitas_real_id = Column(Integer, ForeignKey("entitas._real_id"))

class Entitas(Model):
    __session__ = session
    _father_real_id = Column(Integer, ForeignKey("parent._real_id"))
    _mother_real_id = Column(Integer, ForeignKey("parent._real_id"))
    alamat = Column(String)
    children = relationship("Child", foreign_keys="Child._entitas_real_id")
    father = relationship("Parent", foreign_keys="Entitas._father_real_id")
    mother = relationship("Parent", foreign_keys="Entitas._mother_real_id")
    nama = Column(String)

class Parent(Model):
    __session__ = session


Model.metadata.create_all(bind=engine)