from kokoropy.controller import Crud_Controller
from ..models._all import Theme

class Theme_Controller(Crud_Controller):
    __model__       = Theme

Theme_Controller.publish_route()