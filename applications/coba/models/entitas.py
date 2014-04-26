from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model, auto_migrate
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

class Entitas(Model):
    __session__ = session
    nama = Column(String(50))
    alamat = Column(String(50))
    fk_father = Column(Integer, ForeignKey("parent._real_id"))
    father = relationship("Parent", foreign_keys="Entitas.fk_father")
    fk_mother = Column(Integer, ForeignKey("parent._real_id"))
    mother = relationship("Parent", foreign_keys="Entitas.fk_mother")
    children = relationship("Child", foreign_keys="Child.fk_entitas")

class Parent(Model):
    __session__ = session

class Child(Model):
    __session__ = session
    fk_entitas = Column(Integer, ForeignKey("entitas._real_id"))


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)