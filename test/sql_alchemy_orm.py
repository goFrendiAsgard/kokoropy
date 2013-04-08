# create engine
from kokoropy.sqlalchemy import create_engine
engine = create_engine('sqlite:///orm.db')

# create Base
from kokoropy.sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# create table
from kokoropy.sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

class Address(Base):
    __tablename__ = 'addresses'
    address_id = Column(Integer, primary_key=True)
    user_id = Column(None, ForeignKey('users.id'))
    address = Column(String)
    
    def __init__(self, address):
        self.address = address

user = User('Tono', 'Tono Martono', 'Rahasia')
print (user)