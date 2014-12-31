from kokoropy.controller import Crud_Controller
from ..models._all import G_Table_Name

class G_Table_Name_Controller(Crud_Controller):
    __model__       = G_Table_Name

G_Table_Name_Controller.publish_route()