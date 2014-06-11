from kokoropy.controller import Crud_Controller
from ..models.country import Country

class Country_Controller(Crud_Controller):
    __model__               = Country
    __application_name__    = 'country'
    __view_directory__      = 'country'

Country_Controller.publish_route()