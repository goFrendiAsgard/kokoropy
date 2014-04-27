from kokoropy import Autoroute_Controller, load_view, base_url
from ..models.entitas import Offspring, Parent, Entitas

url_list = {
        'index'   : base_url('coba/entitas/index'),
        'list'    : base_url('coba/entitas/list'),
        'show'    : base_url('coba/entitas/show'),
        'new'     : base_url('coba/entitas/new'),
        'create'  : base_url('coba/entitas/create'),
        'edit'    : base_url('coba/entitas/edit'),
        'update'  : base_url('coba/entitas/update'),
        'trash'   : base_url('coba/entitas/trash'),
        'remove'  : base_url('coba/entitas/remove'),
        'delete'  : base_url('coba/entitas/delete'),
        'destroy' : base_url('coba/entitas/destroy')
    }

class Entitas_Controller(Autoroute_Controller):
    
    def action_index(self):
        return self.action_list()
    
    def action_list(self):
        ''' Show table '''
        entitas_list = Entitas.get()
        return load_view('coba', 'entitas_list', 
             entitas_list = entitas_list, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_show', entitas = entitas,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        entitas = Entitas()
        return load_view('coba', 'entitas_new', entitas = entitas, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        entitas = Entitas()
        # put your code here
        entitas.save()
        success = entitas.success
        error_message = entitas.error_message
        return load_view('coba', 'entitas_create', entitas = entitas,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_edit', entitas = entitas,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        entitas = Entitas.find(id)
        # put your code here
        entitas.save()
        success = entitas.success
        error_message = entitas.error_message
        return load_view('coba', 'entitas_update', entitas = entitas,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_trash', entitas = entitas,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        entitas = Entitas.find(id)
        entitas.trash()
        success = entitas.success
        error_message = entitas.error_message
        return load_view('coba', 'entitas_remove', entitas = entitas,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_delete', entitas = entitas,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        entitas = Entitas.find(id)
        entitas.delete()
        success = entitas.success
        error_message = entitas.error_message
        return load_view('coba', 'entitas_create', entitas = entitas,
            url_list = url_list, success = success, error_message = error_message)