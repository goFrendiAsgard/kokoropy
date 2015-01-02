from kokoropy.controller import Crud_Controller
from ..models._all import Clan

class Clan_Controller(Crud_Controller):
    __model__       = Clan

Clan_Controller.publish_route()