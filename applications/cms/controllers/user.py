from kokoropy.controller import Crud_Controller
from ..models.structure import User

class User_Controller(Crud_Controller):
    __model__               = User

User_Controller.publish_route()