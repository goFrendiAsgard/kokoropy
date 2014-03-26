from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Column, BIGINT, BigInteger, BINARY, Binary,\
    BOOLEAN, Boolean, DATE, Date, DATETIME, DateTime, FLOAT, Float,\
    INTEGER, Integer, VARCHAR, String, TEXT, Text
from ..configs.db import engine

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
    pass