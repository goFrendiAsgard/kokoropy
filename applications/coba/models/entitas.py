from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model, auto_migrate
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

class Entitas(Model):
    __session__ = session
    nama = Column(String(50))
    alamat = Column(String(20))
    tanggal_lahir = Column(DateTime(20))
    children = relationship("Child", foreign_keys="Child.fk_entitas")
    fk_father = Column(Integer, ForeignKey("parent._real_id"))
    father = relationship("Parent", foreign_keys="Entitas.fk_father")
    fk_mother = Column(Integer, ForeignKey("parent._real_id"))
    mother = relationship("Parent", foreign_keys="Entitas.fk_mother")

class Child(Model):
    __session__ = session
    fk_entitas = Column(Integer, ForeignKey("entitas._real_id"))

class Parent(Model):
    __session__ = session

auto_migrate(engine)