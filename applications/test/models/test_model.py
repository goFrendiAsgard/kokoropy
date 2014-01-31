
from sqlalchemy import Column, Integer, String, text, ForeignKey, Table, ForeignKeyConstraint, create_engine
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def test_things():

    # create Base
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        user_id = Column(Integer, primary_key=True)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)
        addresses = relationship('Address', backref='user')
        
        def __init__(self, name, fullname, password, addresses):
            self.name = name
            self.fullname = fullname
            self.password = password
            self.addresses = addresses

    class Address(Base):
        __tablename__ = 'addresses'
        address_id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.user_id'))
        address = Column(String)
        
        def __init__(self, address):
            self.address = address

    # create engine
    engine = create_engine('sqlite:///orm.db', echo=True)    

    #################### ORM ########################################

    # create db session
    db_session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(bind=engine)

    # play with object
    address_1 = Address('Mars')
    address_2 = Address('Jupiter')
    user = User('Tono', 'Tono Martono', 'Rahasia', [address_1, address_2])
    print (user)

    db_session.add(user)
    db_session.commit()

    ################# NON ORM ########################################
    '''
    metadata = MetaData()
    users = Table('users', metadata,
                  Column('user_id', Integer, primary_key=True),
                  Column('name', String),
                  Column('password', String)
            )
    addresses = Table('addresses', metadata,
                  Column('address_id', Integer, primary_key=True),
                  Column('email_address', String),
                  Column('user_id', None, ForeignKey('users.user_id'))
            )

    # create tables on engine based on metadata
    metadata.create_all(engine)
    '''
    # create connection
    conn = engine.connect()

    # insert statement
    sql = '''INSERT INTO users(name, password)
        VALUES(:user_name, :user_password)'''
    conn.execute(text(sql), user_name='Tino', user_password='secret')

    # select statement
    sql = '''SELECT * FROM users'''
    print (conn.execute(text(sql)).fetchall())

if __name__ == '__main__':
    test_things()