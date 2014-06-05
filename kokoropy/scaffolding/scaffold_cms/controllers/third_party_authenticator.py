from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/third_party_authenticator/index'),
        'list'    : base_url('cms/third_party_authenticator/list'),
        'show'    : base_url('cms/third_party_authenticator/show'),
        'new'     : base_url('cms/third_party_authenticator/new'),
        'create'  : base_url('cms/third_party_authenticator/create'),
        'edit'    : base_url('cms/third_party_authenticator/edit'),
        'update'  : base_url('cms/third_party_authenticator/update'),
        'trash'   : base_url('cms/third_party_authenticator/trash'),
        'remove'  : base_url('cms/third_party_authenticator/remove'),
        'delete'  : base_url('cms/third_party_authenticator/delete'),
        'destroy' : base_url('cms/third_party_authenticator/destroy')
    }

class Third_Party_Authenticator_Controller(Autoroute_Controller):
    
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
        third_party_authenticator_list = Third_Party_Authenticator.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Third_Party_Authenticator.count())/limit))
        return load_view('cms', 'third_party_authenticator/list', 
            third_party_authenticator_list = third_party_authenticator_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        third_party_authenticator = Third_Party_Authenticator.find(id)
        third_party_authenticator.set_state_show()
        return load_view('cms', 'third_party_authenticator/show', third_party_authenticator = third_party_authenticator,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        third_party_authenticator = Third_Party_Authenticator()
        third_party_authenticator.set_state_insert()
        return load_view('cms', 'third_party_authenticator/new', third_party_authenticator = third_party_authenticator, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        third_party_authenticator = Third_Party_Authenticator()
        third_party_authenticator.set_state_insert()
        # put your code here
        third_party_authenticator.assign_from_dict(request.POST)
        third_party_authenticator.save()
        success = third_party_authenticator.success
        error_message = third_party_authenticator.error_message
        return load_view('cms', 'third_party_authenticator/create', third_party_authenticator = third_party_authenticator,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        third_party_authenticator = Third_Party_Authenticator.find(id)
        third_party_authenticator.set_state_update()
        return load_view('cms', 'third_party_authenticator/edit', third_party_authenticator = third_party_authenticator,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        third_party_authenticator = Third_Party_Authenticator.find(id)
        third_party_authenticator.set_state_update()
        # put your code here
        third_party_authenticator.assign_from_dict(request.POST)
        third_party_authenticator.save()
        success = third_party_authenticator.success
        error_message = third_party_authenticator.error_message
        return load_view('cms', 'third_party_authenticator/update', third_party_authenticator = third_party_authenticator,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        third_party_authenticator = Third_Party_Authenticator.find(id)
        return load_view('cms', 'third_party_authenticator/trash', third_party_authenticator = third_party_authenticator,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        third_party_authenticator = Third_Party_Authenticator.find(id)
        third_party_authenticator.trash()
        success = third_party_authenticator.success
        error_message = third_party_authenticator.error_message
        return load_view('cms', 'third_party_authenticator/remove', third_party_authenticator = third_party_authenticator,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        third_party_authenticator = Third_Party_Authenticator.find(id)
        return load_view('cms', 'third_party_authenticator/delete', third_party_authenticator = third_party_authenticator,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        third_party_authenticator = Third_Party_Authenticator.find(id)
        third_party_authenticator.delete()
        success = third_party_authenticator.success
        error_message = third_party_authenticator.error_message
        return load_view('cms', 'third_party_authenticator/destroy', third_party_authenticator = third_party_authenticator,
            url_list = url_list, success = success, error_message = error_message)