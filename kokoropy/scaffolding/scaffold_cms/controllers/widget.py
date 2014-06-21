from kokoropy.controller import Crud_Controller
from ..models.structure import Widget

class Widget_Controller(Crud_Controller):
    __model__               = Widget
    __application_name__    = 'cms'
    __view_directory__      = 'widget'

Widget_Controller.publish_route()