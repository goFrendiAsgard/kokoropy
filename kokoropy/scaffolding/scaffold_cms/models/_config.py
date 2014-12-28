from kokoropy.model import create_engine, MetaData, scoped_session, sessionmaker
from ..configs.db import connection_string
import hashlib

class Config:
    __single = None
    def __init__( self, connection_string, *args, **kwargs):
        if Config.__single:
            raise Config.__single
        self.engine = create_engine(connection_string, *args, **kwargs)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.metadata = MetaData()
        Config.__single = self

def create_config(connection_string, *args, **kwargs ):
    try:
        config = Config(connection_string, *args, **kwargs)
    except Config, c:
        config = c
    return config 

config = create_config(connection_string, echo=False)

# use these things in your models
engine   = config.engine
session  = config.session
metadata = config.metadata

authorization_options = {
    'everyone'          : 'Everyone', 
    'authenticated'     : 'Logged in user', 
    'unauthenticated'   : 'Not logged in user',
    'authorized'        : 'Specified member of group and super admin', 
    'strict_authorized' : 'Only specified member of group'
}

def encrypt_password(password):
    return hashlib.md5(hashlib.md5(password).hexdigest()).hexdigest()