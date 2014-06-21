from kokoropy.controller import Crud_Controller
from ..models.structure import G_Table_Name

class G_Table_Name_Controller(Crud_Controller):
    __model__               = G_Table_Name
    __application_name__    = 'g_application_name'
    __view_directory__      = 'g_table_name'

G_Table_Name_Controller.publish_route()