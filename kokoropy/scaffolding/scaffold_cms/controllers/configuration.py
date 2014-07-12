from kokoropy.controller import Crud_Controller
from ..models.structure import Configuration

class Configuration_Controller(Crud_Controller):
    __model__               = Configuration

Configuration_Controller.publish_route()