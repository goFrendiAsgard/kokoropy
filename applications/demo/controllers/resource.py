from kokoropy.controller import Crud_Controller
from ..models._all import Resource

class Resource_Controller(Crud_Controller):
    __model__       = Resource

Resource_Controller.publish_route()