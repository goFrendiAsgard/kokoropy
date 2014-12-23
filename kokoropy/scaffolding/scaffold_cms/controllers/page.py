from kokoropy.controller import Crud_Controller
from ..models._structure import Page

class Page_Controller(Crud_Controller):
    __model__       = Page

Page_Controller.publish_route()