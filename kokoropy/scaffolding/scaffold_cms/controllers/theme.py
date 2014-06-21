from kokoropy.controller import Crud_Controller
from ..models.structure import Theme

class Theme_Controller(Crud_Controller):
    __model__               = Theme
    __application_name__    = 'cms'
    __view_directory__      = 'theme'

Theme_Controller.publish_route()