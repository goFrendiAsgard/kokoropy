from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import DateTime, Column
from ..configs.db import engine

# just a simple upgrade
def upgrade():
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)

    op.add_column('pokemon', Column('last_transaction_date', DateTime))

def downgrade():
    pass