from kokoropy import Autoroute_Controller, load_view
from ..models.entitas import Entitas, Parent, Child

class Entitas_Controller(Autoroute_Controller):
    
    def action_index(self):
        '''
        father = Parent()
        mother = Parent()
        entitas = Entitas()
        entitas.father = father
        entitas.mother = mother
        entitas.children = [Child(), Child()]
        entitas.save()
        print entitas.to_json(include_relation=True)
        print Entitas.get(as_json = True, include_relation = True)
        '''
        entitas_list = Entitas.get()
        return load_view('coba', 'entitas_list', entitas_list = entitas_list)
    
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