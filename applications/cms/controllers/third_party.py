from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.auth import Third_Party, Group, Rel_User_Groups, User, Third_Party_Id
import math

url_list = {
        'index'   : base_url('cms/third_party/index'),
        'list'    : base_url('cms/third_party/list'),
        'show'    : base_url('cms/third_party/show'),
        'new'     : base_url('cms/third_party/new'),
        'create'  : base_url('cms/third_party/create'),
        'edit'    : base_url('cms/third_party/edit'),
        'update'  : base_url('cms/third_party/update'),
        'trash'   : base_url('cms/third_party/trash'),
        'remove'  : base_url('cms/third_party/remove'),
        'delete'  : base_url('cms/third_party/delete'),
        'destroy' : base_url('cms/third_party/destroy')
    }

class Third_Party_Controller(Autoroute_Controller):
    
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
        third_party_list = Third_Party.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Third_Party.count())/limit))
        return load_view('cms', 'third_party_list', 
            third_party_list = third_party_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        third_party = Third_Party.find(id)
        return load_view('cms', 'third_party_show', third_party = third_party,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        third_party = Third_Party()
        return load_view('cms', 'third_party_new', third_party = third_party, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        third_party = Third_Party()
        # put your code here
        third_party.assign(request.POST)
        third_party.save()
        success = third_party.success
        error_message = third_party.error_message
        return load_view('cms', 'third_party_create', third_party = third_party,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        third_party = Third_Party.find(id)
        return load_view('cms', 'third_party_edit', third_party = third_party,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        third_party = Third_Party.find(id)
        # put your code here
        third_party.assign(request.POST)
        third_party.save()
        success = third_party.success
        error_message = third_party.error_message
        return load_view('cms', 'third_party_update', third_party = third_party,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        third_party = Third_Party.find(id)
        return load_view('cms', 'third_party_trash', third_party = third_party,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        third_party = Third_Party.find(id)
        third_party.trash()
        success = third_party.success
        error_message = third_party.error_message
        return load_view('cms', 'third_party_remove', third_party = third_party,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        third_party = Third_Party.find(id)
        return load_view('cms', 'third_party_delete', third_party = third_party,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        third_party = Third_Party.find(id)
        third_party.delete()
        success = third_party.success
        error_message = third_party.error_message
        return load_view('cms', 'third_party_create', third_party = third_party,
            url_list = url_list, success = success, error_message = error_message)