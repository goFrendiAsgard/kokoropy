from kokoropy.controller import Crud_Controller
from ..models._structure import Third_Party_Authenticator

class Third_Party_Authenticator_Controller(Crud_Controller):
    __model__       = Third_Party_Authenticator

Third_Party_Authenticator_Controller.publish_route()