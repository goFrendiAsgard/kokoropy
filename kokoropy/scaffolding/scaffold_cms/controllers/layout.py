from kokoropy.controller import Crud_Controller
from ..models.structure import Layout

class Layout_Controller(Crud_Controller):
    __model__               = Layout
    __application_name__    = 'cms'
    __view_directory__      = 'layout'

Layout_Controller.publish_route()