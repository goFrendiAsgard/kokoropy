from sqlalchemy import create_engine, Column, ForeignKey, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from kokoropy.model import Mixin
from applications.coba.configs.db import connection_string

# create Base
Base = declarative_base()
engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

class Pegawai(Base, Mixin):
    __tablename__ = 'pegawai'
    __session__ = session
    nama = Column(String)
    tanggal_lahir = Column(DateTime)

class Alamat(Base, Mixin):
    __tablename__ = 'alamat'
    __session__ = session
    jalan = Column(String)

Base.metadata.create_all(bind=engine)