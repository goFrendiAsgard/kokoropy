from kokoropy.controller import Crud_Controller
from ..models.structure import Language_Detail

class Language_Detail_Controller(Crud_Controller):
    __model__               = Language_Detail
    __application_name__    = 'cms'
    __view_directory__      = 'language_detail'

Language_Detail_Controller.publish_route()