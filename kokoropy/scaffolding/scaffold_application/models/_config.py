from kokoropy.model import BaseConfig
from ..configs.db import connection_string

# create Config class to ensure there is only one engine, session, and metadata accross models
class Config(BaseConfig):
    pass
config = Config(connection_string, echo=False)

# use these things in your models
engine   = config.engine
session  = config.session
metadata = config.metadata