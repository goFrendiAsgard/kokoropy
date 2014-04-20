from kokoropy import Autoroute_Controller, load_view
from ..models.entitas import Child, Parent, Entitas

class Entitas_Controller(Autoroute_Controller):
    
    def action_index(self):
        return self.action_list()
    
    def action_list(self):
        ''' Show table '''
        entitas_list = Entitas.get()
        return load_view('coba', 'entitas_list', entitas_list = entitas_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        pass
    
    def action_new(self):
        ''' Insert Form '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_new', entitas = entitas)
    
    def action_create(self):
        ''' Insert Action '''
        entitas = Entitas()
        # put your code here
        entitas.save()
    
    def action_edit(self, id):
        ''' Update Form '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_edit', entitas = entitas)
    
    def action_update(self,id):
        ''' Update Action '''
        entitas = Entitas.find(row_id)
        # put your code here
        entitas.save()
    
    def action_trash(self, id):
        ''' Trash Form '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_trash', entitas = entitas)
    
    def action_remove(self, id):
        ''' Trash Action '''
        entitas = Entitas.find(id)
        entitas.trash()
    
    def action_delete(self, id):
        ''' Delete Form '''
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_delete', entitas = entitas)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        entitas = Entitas.find(id)
        entitas.delete()