from os.path import dirname
from os.path import join as path_join

# connection string
# By default, we use sqlite. However you can change the connection string
# so that you can also use mysql, postgresql, etc.
# below is the example of mysql's connection string:
# mysql://user:password@server/schema
connection_string = 'sqlite:///' + path_join(dirname(dirname(__file__)), 'db', 'database.db')