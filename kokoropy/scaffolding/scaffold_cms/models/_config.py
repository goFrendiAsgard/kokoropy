from kokoropy.model import create_engine, MetaData, scoped_session, sessionmaker, BaseConfig
from ..configs.db import connection_string
import hashlib

# create Config class to ensure there is only one engine, session, and metadata accross models
class Config(BaseConfig):
    pass
config = Config(connection_string, echo=False)

# use these things in your models
engine   = config.engine
session  = config.session
metadata = config.metadata

authorization_options = {
    'everyone'          : 'Everyone', 
    'authenticated'     : 'Logged in user', 
    'unauthenticated'   : 'Not logged in user',
    'authorized'        : 'Specified member of group or super admin', 
    'strict_authorized' : 'Only specified member of group'
}

def encrypt_password(password):
    return hashlib.md5(hashlib.md5(password).hexdigest()).hexdigest()