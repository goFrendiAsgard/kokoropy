from kokoropy.controller import Crud_Controller
from ..models.structure import Language

class Language_Controller(Crud_Controller):
    __model__               = Language
    __application_name__    = 'cms'
    __view_directory__      = 'language'

Language_Controller.publish_route()