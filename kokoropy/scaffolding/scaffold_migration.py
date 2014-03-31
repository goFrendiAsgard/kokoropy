from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, Column, BIGINT, BigInteger, BINARY, Binary,\
    BOOLEAN, Boolean, DATE, Date, DATETIME, DateTime, FLOAT, Float,\
    INTEGER, Integer, VARCHAR, String, TEXT, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from ..configs.db import connection_string

# create engine
engine = create_engine(connection_string, echo=True)

# create db session
db_session = scoped_session(sessionmaker(bind=engine))

conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

signature = 'g_timestamp'

# just a simple upgrade
def upgrade():    
    '''
    # create table:
        op.create_table(
            'table_name',
            Column('id', INTEGER, primary_key = True),
            Column('name', VARCHAR(50), nullable = False)
        )
    # add column:
        op.add_column('table_name', Column('user_name', String))
    # alter_column:
        op.alter_column('table_name', 'name', nullable = True)
    '''
    # g_add_column
    pass

def downgrade():
    '''
    # drop table:
        op.drop_table('table_name')
    # drop_column:
        op.drop_column('table_name', 'user_name')
    # alter_column
        op.alter_column('table_name', 'name', nullable = False)
    '''
    # g_drop_column
    pass