from kokoropy.controller import Crud_Controller
from ..models.structure import Political_View

class Political_View_Controller(Crud_Controller):
    __model__               = Political_View
    __application_name__    = 'country'
    __view_directory__      = 'political_view'

Political_View_Controller.publish_route()