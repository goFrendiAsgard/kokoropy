from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

############################### SQL ALCHEMY SCRIPT ####################################

# create Base
Base = declarative_base()

# create Pokemon class
class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    
    def __init__(self, name, image):
        self.name = name
        self.image = image

# create engine
engine = create_engine('sqlite:///db/pokemon.db', echo=True)

# create db session
db_session = scoped_session(sessionmaker(bind=engine))

class Db_Model(object):
    '''
    Create, Update & Delete Pokemon data
    '''
    def __init__(self):
        Base.metadata.create_all(bind=engine)
    
    def get_pokemon_by_id(self, pokemon_id):
        return db_session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    
    def get_pokemon(self, keyword=''):
        return db_session.query(Pokemon).filter(Pokemon.name.like('%'+keyword+'%')).all()
    
    def delete_pokemon(self, pokemon_id):
        pokemon = self.get_pokemon_by_id(pokemon_id)
        db_session.remove(pokemon)
        db_session.commit()
    
    def insert_pokemon(self, name, image=''):
        pokemon = Pokemon(name, image)
        db_session.add(pokemon)
        db_session.commit()
    
    def update_pokemon(self, pokemon_id, name, image=''):
        pokemon = self.get_pokemon_by_id(pokemon_id)
        pokemon.name = name
        pokemon.image = image
        db_session.commit()
