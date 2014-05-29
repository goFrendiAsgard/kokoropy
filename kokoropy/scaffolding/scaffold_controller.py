from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.g_model_module import G_Table_Name_List
import math

url_list = {
        'index'   : base_url('g_application_name/g_table_name/index'),
        'list'    : base_url('g_application_name/g_table_name/list'),
        'show'    : base_url('g_application_name/g_table_name/show'),
        'new'     : base_url('g_application_name/g_table_name/new'),
        'create'  : base_url('g_application_name/g_table_name/create'),
        'edit'    : base_url('g_application_name/g_table_name/edit'),
        'update'  : base_url('g_application_name/g_table_name/update'),
        'trash'   : base_url('g_application_name/g_table_name/trash'),
        'remove'  : base_url('g_application_name/g_table_name/remove'),
        'delete'  : base_url('g_application_name/g_table_name/delete'),
        'destroy' : base_url('g_application_name/g_table_name/destroy')
    }

class G_Table_Name_Controller(Autoroute_Controller):
    
    def action_index(self):
        return self.action_list()
    
    def action_list(self):
        ''' Show table '''
        # get page index
        current_page = int(request.GET['page']) if 'page' in request.GET else 1
        # determine limit and offset
        limit = 50
        offset = (current_page-1) * limit
        # get the data
        g_table_name_list = G_Table_Name.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(G_Table_Name.count())/limit))
        return load_view('g_application_name', 'g_table_name_list', 
            g_table_name_list = g_table_name_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        g_table_name = G_Table_Name.find(id)
        g_table_name.set_state_show()
        return load_view('g_application_name', 'g_table_name_show', g_table_name = g_table_name,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        g_table_name = G_Table_Name()
        g_table_name.set_state_insert()
        return load_view('g_application_name', 'g_table_name_new', g_table_name = g_table_name, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        g_table_name = G_Table_Name()
        g_table_name.set_state_insert()
        # put your code here
        g_table_name.assign_from_dict(request.POST)
        g_table_name.save()
        success = g_table_name.success
        error_message = g_table_name.error_message
        return load_view('g_application_name', 'g_table_name_create', g_table_name = g_table_name,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        g_table_name = G_Table_Name.find(id)
        g_table_name.set_state_update()
        return load_view('g_application_name', 'g_table_name_edit', g_table_name = g_table_name,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        g_table_name = G_Table_Name.find(id)
        g_table_name.set_state_update()
        # put your code here
        g_table_name.assign_from_dict(request.POST)
        g_table_name.save()
        success = g_table_name.success
        error_message = g_table_name.error_message
        return load_view('g_application_name', 'g_table_name_update', g_table_name = g_table_name,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        g_table_name = G_Table_Name.find(id)
        return load_view('g_application_name', 'g_table_name_trash', g_table_name = g_table_name,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        g_table_name = G_Table_Name.find(id)
        g_table_name.trash()
        success = g_table_name.success
        error_message = g_table_name.error_message
        return load_view('g_application_name', 'g_table_name_remove', g_table_name = g_table_name,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        g_table_name = G_Table_Name.find(id)
        return load_view('g_application_name', 'g_table_name_delete', g_table_name = g_table_name,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        g_table_name = G_Table_Name.find(id)
        g_table_name.delete()
        success = g_table_name.success
        error_message = g_table_name.error_message
        return load_view('g_application_name', 'g_table_name_create', g_table_name = g_table_name,
            url_list = url_list, success = success, error_message = error_message)