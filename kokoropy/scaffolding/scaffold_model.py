from sqlalchemy import or_, and_, create_engine, MetaData, Column, ForeignKey, func, \
    Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model, auto_migrate
from ..configs.db import connection_string

engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

DB_Model.metadata = MetaData()

'''
    DB_Model has several commonly overriden property and methods:
    * __excluded_shown_column__           : list, hidden columns on "show detail" (e.g: ["id"])
    * __excluded_insert_column__          : list, hidden columns on "insert form" (e.g: ["id"])
    * __excluded_update_column__          : list, hidden columns on "edit form" (e.g: ["id"])
    * __prefix_of_id__                    : string, prefix id (e.g: "%Y-")
    * __digit_num_of_id__                 : integer, digit count after prefix id (e.g: 4)
    * __column_label__                    : dictionary, label of columns
    * build_input_COLUMN_NAME             : function with one parameter, **kwargs build column input for COLUMN_NAME
    * build_representation_COLUMN_NAME    : function with one parameter, **kwargs build column representation for COLUMN_NAME
    * build_label_COLUMN_NAME             : function with one parameter, **kwargs build column label for COLUMN_NAME
'''

# g_structure
'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on DB_Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)