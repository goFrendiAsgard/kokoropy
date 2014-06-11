from kokoropy.controller import Crud_Controller
from ..models.country import City

class City_Controller(Crud_Controller):
    __model__               = City
    __application_name__    = 'country'
    __view_directory__      = 'city'

City_Controller.publish_route()