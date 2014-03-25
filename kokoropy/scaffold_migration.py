from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Column, BigInteger, Binary, Boolean, Date, DateTime, Float, Integer, String, Text
from ..configs.db import engine

conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

def timestamp():
    return 'g_timestamp'

# just a simple upgrade
def upgrade():    
    #op.add_column('table_name', Column('column_name', ColumnType))
    pass

def downgrade():
    pass