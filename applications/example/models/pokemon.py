from kokoropy.model import DB_Model, auto_migrate, base_url, Column, or_, and_, create_engine, MetaData, ForeignKey, func, \
    Integer, String, Date, DateTime, Boolean, Upload, Text, scoped_session, sessionmaker, relationship, backref, association_proxy
from ..configs.db import connection_string
from kokoropy import save_uploaded_asset, request
import os


engine = create_engine(connection_string, echo=False)
session = scoped_session(sessionmaker(bind=engine))

DB_Model.metadata = MetaData()

class Pokemon(DB_Model):
    __session__ = session
    __prefix_of_id__ = 'pokemon-'
    __automatic_assigned_column__ = ['id','name']
    # Fields Declarations
    name = Column(String(50))
    image = Column(Upload(50, is_image = True))

    def quick_preview(self):
        if self.is_list_state():
            return self.build_representation('image') + '<br />' + self.name
        return self.name


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on DB_Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)
if Pokemon.count() == 0:
    for pokemon_name in ['bubasaur', 'caterpie', 'charmender', 'pikachu', 'squirtle']:
        pokemon = Pokemon()
        pokemon.name = pokemon_name
        pokemon.image = pokemon_name + '.png'
        pokemon.save()