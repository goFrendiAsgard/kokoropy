from kokoropy import Autoroute_Controller, load_view
from ..models.g_table_name import G_Table_Name_List

class G_Table_Name_Controller(Autoroute_Controller):
    
    def action_index(self):
        g_table_name_list = G_Table_Name.get()
        return load_view('g_application_name', 'g_table_name', g_table_name_list = g_table_name_list)
    
    def action_list(self):
        g_table_name_list = G_Table_Name.get(as_json = True, include_relation = False)
        return load_view('g_application_name', 'g_table_name_list', g_table_name_list = g_table_name_list)
    
    def action_form_insert(self):
        return load_view('g_application_name', 'g_table_name_form_insert')
    
    def action_form_update(self, id):
        g_table_name = G_Table_Name.find(id)
        return load_view('g_application_name', 'g_table_name_form_insert', g_table_name = g_table_name)
    
    def action_insert(self):
        g_table_name = G_Table_Name()
        # put your code here
        g_table_name.save()
    
    def action_update(self, row_id):
        g_table_name = G_Table_Name.find(row_id)
        # put your code here
        g_table_name.save()
    
    def action_delete(self, row_id):
        g_table_name = G_Table_Name.find(row_id)
        # put your code here
        g_table_name.delete()