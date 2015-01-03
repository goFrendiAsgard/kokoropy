from kokoropy.controller import Crud_Controller
from ..models._all import Widget

class Widget_Controller(Crud_Controller):
    __model__       = Widget

Widget_Controller.publish_route()