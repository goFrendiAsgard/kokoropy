from kokoropy.controller import Crud_Controller
from ..models.structure import Configuration

class Configuration_Controller(Crud_Controller):
    __model__               = Configuration
    __application_name__    = 'cms'
    __view_directory__      = 'configuration'

Configuration_Controller.publish_route()