from kokoropy.controller import Crud_Controller
from ..models._structure import Cms

class Cms_Controller(Crud_Controller):
    __model__       = Cms

Cms_Controller.publish_route()