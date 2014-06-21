from kokoropy.controller import Crud_Controller
from ..models.structure import Cms

class Cms_Controller(Crud_Controller):
    __model__               = Cms
    __application_name__    = 'cms'
    __view_directory__      = 'cms'

Cms_Controller.publish_route()