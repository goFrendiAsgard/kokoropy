from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

class Entitas(Model):
    __session__ = session
    nama = Column(String)
    alamat = Column(String)
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


Model.metadata.create_all(bind=engine)
for table_name in Model.metadata.tables:
    print table_name
    table = Model.metadata.tables[table_name]
    for column in table.columns:
        print column, column.name, column.type