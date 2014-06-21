from kokoropy.controller import Crud_Controller
from ..models.structure import User

class User_Controller(Crud_Controller):
    __model__               = User
    __application_name__    = 'cms'
    __view_directory__      = 'user'

User_Controller.publish_route()