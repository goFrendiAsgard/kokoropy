from sqlalchemy import create_engine, Column, func, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from kokoropy.Model import Mixin
from ..config.db import connection_string

# create Base
Base = declarative_base()

class G_Table_Name(Base, Mixin):
    __tablename__ = 'g_table_name'
    __connectionstring__ = connection_string
    __echo__ = False
    g_fields = Column(String)