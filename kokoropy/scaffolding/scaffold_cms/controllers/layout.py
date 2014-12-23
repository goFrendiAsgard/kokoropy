from kokoropy.controller import Crud_Controller
from ..models._structure import Layout

class Layout_Controller(Crud_Controller):
    __model__       = Layout

Layout_Controller.publish_route()