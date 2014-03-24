# just a simple upgrade
def upgrade():
    from alembic.migration import MigrationContext
    from alembic.operations import Operations
    from sqlalchemy import DateTime
    from ..configs.db import engine

    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)

    op.add_column('pokemon', Column('last_transaction_date', DateTime))