from kokoropy import Autoroute_Controller, load_view, base_url
from ..models.orang import Orang, Pekerjaan, Jurus, Hobi, Association_Orang_Hobi

url_list = {
        'index'   : base_url('coba/orang/index'),
        'list'    : base_url('coba/orang/list'),
        'show'    : base_url('coba/orang/show'),
        'new'     : base_url('coba/orang/new'),
        'create'  : base_url('coba/orang/create'),
        'edit'    : base_url('coba/orang/edit'),
        'update'  : base_url('coba/orang/update'),
        'trash'   : base_url('coba/orang/trash'),
        'remove'  : base_url('coba/orang/remove'),
        'delete'  : base_url('coba/orang/delete'),
        'destroy' : base_url('coba/orang/destroy')
    }

class Orang_Controller(Autoroute_Controller):
    
    def action_index(self):
        return self.action_list()
    
    def action_list(self):
        ''' Show table '''
        orang_list = Orang.get()
        return load_view('coba', 'orang_list', 
             orang_list = orang_list, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        orang = Orang.find(id)
        return load_view('coba', 'orang_show', orang = orang,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        orang = Orang()
        return load_view('coba', 'orang_new', orang = orang, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        orang = Orang()
        # put your code here
        orang.save()
        success = orang.success
        error_message = orang.error_message
        return load_view('coba', 'orang_create', orang = orang,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        orang = Orang.find(id)
        return load_view('coba', 'orang_edit', orang = orang,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        orang = Orang.find(id)
        # put your code here
        orang.save()
        success = orang.success
        error_message = orang.error_message
        return load_view('coba', 'orang_update', orang = orang,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        orang = Orang.find(id)
        return load_view('coba', 'orang_trash', orang = orang,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        orang = Orang.find(id)
        orang.trash()
        success = orang.success
        error_message = orang.error_message
        return load_view('coba', 'orang_remove', orang = orang,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        orang = Orang.find(id)
        return load_view('coba', 'orang_delete', orang = orang,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        orang = Orang.find(id)
        orang.delete()
        success = orang.success
        error_message = orang.error_message
        return load_view('coba', 'orang_create', orang = orang,
            url_list = url_list, success = success, error_message = error_message)