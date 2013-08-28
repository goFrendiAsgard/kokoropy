# create engine
from kokoropy.sqlalchemy import create_engine
engine = create_engine('sqlite:///non_orm.db', echo=True)

# create metadata of table schemas
from kokoropy.sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
metadata = MetaData()
users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True),
              Column('user_name', String),
              Column('user_password', String)
        )
addresses = Table('addresses', metadata,
              Column('address_id', Integer, primary_key=True),
              Column('email_address', String),
              Column('user_id', None, ForeignKey('users.user_id'))
        )

# create tables on engine based on metadata
metadata.create_all(engine)

# connect
conn = engine.connect()
from kokoropy.sqlalchemy import text

# insert statement
sql = '''INSERT INTO users(user_name, user_password)
    VALUES(:user_name, :user_password)'''
conn.execute(text(sql), user_name='Tono', user_password='secret')

# select statement
sql = '''SELECT * FROM users'''
print (conn.execute(text(sql)).fetchall())

