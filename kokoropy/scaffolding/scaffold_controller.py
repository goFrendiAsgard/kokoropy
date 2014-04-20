from kokoropy import Autoroute_Controller, load_view
from ..models.g_table_name import G_Table_Name_List

class G_Table_Name_Controller(Autoroute_Controller):
    
    def action_index(self):
        return self.action_list()
    
    def action_list(self):
        ''' Show table '''
        g_table_name_list = G_Table_Name.get()
        return load_view('g_application_name', 'g_table_name_list', g_table_name_list = g_table_name_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        pass
    
    def action_new(self):
        ''' Insert Form '''
        g_table_name = G_Table_Name.find(id)
        return load_view('g_application_name', 'g_table_name_new', g_table_name = g_table_name)
    
    def action_create(self):
        ''' Insert Action '''
        g_table_name = G_Table_Name()
        # put your code here
        g_table_name.save()
    
    def action_edit(self, id):
        ''' Update Form '''
        g_table_name = G_Table_Name.find(id)
        return load_view('g_application_name', 'g_table_name_edit', g_table_name = g_table_name)
    
    def action_update(self,id):
        ''' Update Action '''
        g_table_name = G_Table_Name.find(row_id)
        # put your code here
        g_table_name.save()
    
    def action_trash(self, id):
        ''' Trash Form '''
        g_table_name = G_Table_Name.find(id)
        return load_view('g_application_name', 'g_table_name_trash', g_table_name = g_table_name)
    
    def action_remove(self, id):
        ''' Trash Action '''
        g_table_name = G_Table_Name.find(id)
        g_table_name.trash()
    
    def action_delete(self, id):
        ''' Delete Form '''
        g_table_name = G_Table_Name.find(id)
        return load_view('g_application_name', 'g_table_name_delete', g_table_name = g_table_name)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        g_table_name = G_Table_Name.find(id)
        g_table_name.delete()