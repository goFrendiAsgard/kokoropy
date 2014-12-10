from kokoropy.model import DB_Model, auto_migrate
from _config import engine

# g_import

'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on DB_Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)