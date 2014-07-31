from kokoropy.controller import Crud_Controller
from ..models.structure import Language

class Language_Controller(Crud_Controller):
    __model__               = Language

Language_Controller.publish_route()