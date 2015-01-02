from kokoropy.controller import Crud_Controller
from ..models._all import Village

class Village_Controller(Crud_Controller):
    __model__       = Village

Village_Controller.publish_route()