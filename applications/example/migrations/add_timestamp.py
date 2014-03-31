from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from ..configs.db import connection_string

# create engine
engine = create_engine(connection_string, echo=True)

# create db session
db_session = scoped_session(sessionmaker(bind=engine))
conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)
signature = '2013'

# just a simple upgrade
def upgrade():    
    op.add_column('pokemon', Column('last_transaction_date', DateTime))

def downgrade():
    pass