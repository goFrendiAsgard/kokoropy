from kokoropy.controller import Crud_Controller
from ..models._structure import Language_Detail

class Language_Detail_Controller(Crud_Controller):
    __model__       = Language_Detail

Language_Detail_Controller.publish_route()