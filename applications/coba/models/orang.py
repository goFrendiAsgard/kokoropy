from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from kokoropy.model import Model, auto_migrate
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

class Orang(Model):
    __session__ = session
    nama = Column(String(50))
    alamat = Column(String(50))
    fk_ayah = Column(Integer, ForeignKey("orang._real_id"))
    ayah = relationship("Orang", foreign_keys="Orang.fk_ayah")
    fk_ibu = Column(Integer, ForeignKey("orang._real_id"))
    ibu = relationship("Orang", foreign_keys="Orang.fk_ibu")
    fk_orang = Column(Integer, ForeignKey("orang._real_id"))
    teman = relationship("Orang", foreign_keys="Orang.fk_orang")
    fk_orang_1 = Column(Integer, ForeignKey("orang._real_id"))
    anak = relationship("Orang", foreign_keys="Orang.fk_orang_1")
    jurus = relationship("Jurus", foreign_keys="Jurus.fk_orang")
    fk_pekerjaan = Column(Integer, ForeignKey("pekerjaan._real_id"))
    pekerjaan = relationship("Pekerjaan", foreign_keys="Orang.fk_pekerjaan")
    hobi = relationship("Association_Orang_Hobi", foreign_keys="Association_Orang_Hobi.fk_orang")
    tanggal_lahir = Column(Date)

class Jurus(Model):
    __session__ = session
    fk_orang = Column(Integer, ForeignKey("orang._real_id"))

class Pekerjaan(Model):
    __session__ = session

class Hobi(Model):
    __session__ = session

class Association_Orang_Hobi(Model):
    __session__ = session
    fk_orang = Column(Integer, ForeignKey("orang._real_id"))
    fk_hobi = Column(Integer, ForeignKey("hobi._real_id"))
    hobi = relationship("Hobi", foreign_keys="Association_Orang_Hobi.fk_hobi")


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)