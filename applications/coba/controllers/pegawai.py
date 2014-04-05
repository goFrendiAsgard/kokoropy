from kokoropy import Autoroute_Controller, load_view
from ..models.pegawai import Pegawai

class Pegawai_Controller(Autoroute_Controller):
    
    def action_index(self):
        pegawai_list = Pegawai.get()
        return load_view('coba', 'pegawai_list', pegawai_list = pegawai_list)
    
    def action_insert(self):
        pegawai = Pegawai()
        # put your code here
        pegawai.save()
    
    def action_update(self, row_id):
        pegawai = Pegawai.find(row_id)
        # put your code here
        pegawai.save()
    
    def action_delete(self, row_id):
        pegawai = Pegawai.find(row_id)
        # put your code here
        pegawai.delete()