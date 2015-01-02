from kokoropy.model import DB_Model, auto_migrate
from _config import engine

from village import Village, Village_Friends, Village_Commodities
from clan import Clan
from resource import Resource
from villager import Villager
from structure import Structure


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on DB_Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)