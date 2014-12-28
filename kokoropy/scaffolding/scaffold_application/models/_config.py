from kokoropy.model import create_engine, MetaData, scoped_session, sessionmaker
from ..configs.db import connection_string

# singleton class Config
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