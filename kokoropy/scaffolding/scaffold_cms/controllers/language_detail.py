from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/language_detail/index'),
        'list'    : base_url('cms/language_detail/list'),
        'show'    : base_url('cms/language_detail/show'),
        'new'     : base_url('cms/language_detail/new'),
        'create'  : base_url('cms/language_detail/create'),
        'edit'    : base_url('cms/language_detail/edit'),
        'update'  : base_url('cms/language_detail/update'),
        'trash'   : base_url('cms/language_detail/trash'),
        'remove'  : base_url('cms/language_detail/remove'),
        'delete'  : base_url('cms/language_detail/delete'),
        'destroy' : base_url('cms/language_detail/destroy')
    }

class Language_Detail_Controller(Autoroute_Controller):
    
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
        language_detail_list = Language_Detail.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Language_Detail.count())/limit))
        return load_view('cms', 'language_detail/list', 
            language_detail_list = language_detail_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        language_detail = Language_Detail.find(id)
        language_detail.set_state_show()
        return load_view('cms', 'language_detail/show', language_detail = language_detail,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        language_detail = Language_Detail()
        language_detail.set_state_insert()
        return load_view('cms', 'language_detail/new', language_detail = language_detail, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        language_detail = Language_Detail()
        language_detail.set_state_insert()
        # put your code here
        language_detail.assign_from_dict(request.POST)
        language_detail.save()
        success = language_detail.success
        error_message = language_detail.error_message
        return load_view('cms', 'language_detail/create', language_detail = language_detail,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        language_detail = Language_Detail.find(id)
        language_detail.set_state_update()
        return load_view('cms', 'language_detail/edit', language_detail = language_detail,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        language_detail = Language_Detail.find(id)
        language_detail.set_state_update()
        # put your code here
        language_detail.assign_from_dict(request.POST)
        language_detail.save()
        success = language_detail.success
        error_message = language_detail.error_message
        return load_view('cms', 'language_detail/update', language_detail = language_detail,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        language_detail = Language_Detail.find(id)
        return load_view('cms', 'language_detail/trash', language_detail = language_detail,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        language_detail = Language_Detail.find(id)
        language_detail.trash()
        success = language_detail.success
        error_message = language_detail.error_message
        return load_view('cms', 'language_detail/remove', language_detail = language_detail,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        language_detail = Language_Detail.find(id)
        return load_view('cms', 'language_detail/delete', language_detail = language_detail,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        language_detail = Language_Detail.find(id)
        language_detail.delete()
        success = language_detail.success
        error_message = language_detail.error_message
        return load_view('cms', 'language_detail/destroy', language_detail = language_detail,
            url_list = url_list, success = success, error_message = error_message)