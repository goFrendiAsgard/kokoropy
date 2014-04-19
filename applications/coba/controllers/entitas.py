from kokoropy import Autoroute_Controller, load_view
from ..models.entitas import Child, Parent, Entitas

class Entitas_Controller(Autoroute_Controller):
    
    def action_index(self):
        entitas_list = Entitas.get()
        return load_view('coba', 'entitas', entitas_list = entitas_list)
    
    def action_list(self):
        entitas_list = Entitas.get(as_json = True, include_relation = False)
        return load_view('coba', 'entitas_list', entitas_list = entitas_list)
    
    def action_form_insert(self):
        return load_view('coba', 'entitas_form_insert')
    
    def action_form_update(self, id):
        entitas = Entitas.find(id)
        return load_view('coba', 'entitas_form_update', entitas = entitas)
    
    def action_insert(self):
        entitas = Entitas()
        # put your code here
        entitas.save()
    
    def action_update(self, row_id):
        entitas = Entitas.find(row_id)
        # put your code here
        entitas.save()
    
    def action_delete(self, row_id):
        entitas = Entitas.find(row_id)
        # put your code here
        entitas.delete()