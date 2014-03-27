from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import DateTime, Column
from ..configs.db import engine

conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)
signature = '2013'

# just a simple upgrade
def upgrade():    
    op.add_column('pokemon', Column('last_transaction_date', DateTime))

def downgrade():
    pass