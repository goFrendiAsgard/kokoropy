from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/language/index'),
        'list'    : base_url('cms/language/list'),
        'show'    : base_url('cms/language/show'),
        'new'     : base_url('cms/language/new'),
        'create'  : base_url('cms/language/create'),
        'edit'    : base_url('cms/language/edit'),
        'update'  : base_url('cms/language/update'),
        'trash'   : base_url('cms/language/trash'),
        'remove'  : base_url('cms/language/remove'),
        'delete'  : base_url('cms/language/delete'),
        'destroy' : base_url('cms/language/destroy')
    }

class Language_Controller(Autoroute_Controller):
    
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
        language_list = Language.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Language.count())/limit))
        return load_view('cms', 'language/list', 
            language_list = language_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        language = Language.find(id)
        language.set_state_show()
        return load_view('cms', 'language/show', language = language,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        language = Language()
        language.set_state_insert()
        return load_view('cms', 'language/new', language = language, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        language = Language()
        language.set_state_insert()
        # put your code here
        language.assign_from_dict(request.POST)
        language.save()
        success = language.success
        error_message = language.error_message
        return load_view('cms', 'language/create', language = language,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        language = Language.find(id)
        language.set_state_update()
        return load_view('cms', 'language/edit', language = language,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        language = Language.find(id)
        language.set_state_update()
        # put your code here
        language.assign_from_dict(request.POST)
        language.save()
        success = language.success
        error_message = language.error_message
        return load_view('cms', 'language/update', language = language,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        language = Language.find(id)
        return load_view('cms', 'language/trash', language = language,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        language = Language.find(id)
        language.trash()
        success = language.success
        error_message = language.error_message
        return load_view('cms', 'language/remove', language = language,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        language = Language.find(id)
        return load_view('cms', 'language/delete', language = language,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        language = Language.find(id)
        language.delete()
        success = language.success
        error_message = language.error_message
        return load_view('cms', 'language/destroy', language = language,
            url_list = url_list, success = success, error_message = error_message)