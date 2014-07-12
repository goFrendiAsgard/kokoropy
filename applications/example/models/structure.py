from sqlalchemy import or_, and_, create_engine, MetaData, Column, ForeignKey, func, \
    Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model, auto_migrate, base_url
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
    image = Column(String(50))
    
    def before_save(self):
        upload =  request.files.get('image')
        if upload is not None:
            _, ext = os.path.splitext(upload.filename)
            if ext in ('.png','.jpg','.jpeg'):
                save_uploaded_asset('image', path='uploads', application_name = self.__application_name__)
                self.image = upload.filename
    
    def build_input_image(self, **kwargs):
        value = self.build_representation_image()
        return self.build_representation_image() + '<br /><input type="file" name="image" class="_file-input">'
    
    def build_representation_image(self, **kwargs):
        value = self.image
        if value is None:
            value = 'images/pokemon-no-image.png'
        else:
            value = 'uploads/'+value
        return '<img src="' + base_url(self.__application_name__+ '/assets/' + value) + '" style="max-width:100px;" />'
    
    def quick_preview(self):
        print self.state
        if self.is_list_state():
            return self.build_representation_image() + '<br />' + self.name
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