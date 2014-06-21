from kokoropy.controller import Crud_Controller
from ..models.structure import Third_Party_Authenticator

class Third_Party_Authenticator_Controller(Crud_Controller):
    __model__               = Third_Party_Authenticator
    __application_name__    = 'cms'
    __view_directory__      = 'third_party_authenticator'

Third_Party_Authenticator_Controller.publish_route()