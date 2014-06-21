from kokoropy.controller import Crud_Controller
from ..models.structure import Page

class Page_Controller(Crud_Controller):
    __model__               = Page
    __application_name__    = 'cms'
    __view_directory__      = 'page'

Page_Controller.publish_route()