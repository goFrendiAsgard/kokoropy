from kokoropy.controller import Crud_Controller
from ..models.structure import Commodity

class Commodity_Controller(Crud_Controller):
    __model__               = Commodity
    __application_name__    = 'country'
    __view_directory__      = 'commodity'

Commodity_Controller.publish_route()