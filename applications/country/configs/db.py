from os.path import dirname
from os.path import join as path_join

# connection string
connection_string = 'sqlite:///' + path_join(dirname(dirname(__file__)), 'db', 'database.db')