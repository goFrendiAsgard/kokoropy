from kokoropy.controller import Crud_Controller
from ..models.structure import Pokemon

class Pokemon_Controller(Crud_Controller):
    __model__       = Pokemon
    __base_view__   = 'index/views/base'

Pokemon_Controller.publish_route()