from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/theme/index'),
        'list'    : base_url('cms/theme/list'),
        'show'    : base_url('cms/theme/show'),
        'new'     : base_url('cms/theme/new'),
        'create'  : base_url('cms/theme/create'),
        'edit'    : base_url('cms/theme/edit'),
        'update'  : base_url('cms/theme/update'),
        'trash'   : base_url('cms/theme/trash'),
        'remove'  : base_url('cms/theme/remove'),
        'delete'  : base_url('cms/theme/delete'),
        'destroy' : base_url('cms/theme/destroy')
    }

class Theme_Controller(Autoroute_Controller):
    
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
        theme_list = Theme.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Theme.count())/limit))
        return load_view('cms', 'theme/list', 
            theme_list = theme_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        theme = Theme.find(id)
        theme.set_state_show()
        return load_view('cms', 'theme/show', theme = theme,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        theme = Theme()
        theme.set_state_insert()
        return load_view('cms', 'theme/new', theme = theme, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        theme = Theme()
        theme.set_state_insert()
        # put your code here
        theme.assign_from_dict(request.POST)
        theme.save()
        success = theme.success
        error_message = theme.error_message
        return load_view('cms', 'theme/create', theme = theme,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        theme = Theme.find(id)
        theme.set_state_update()
        return load_view('cms', 'theme/edit', theme = theme,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        theme = Theme.find(id)
        theme.set_state_update()
        # put your code here
        theme.assign_from_dict(request.POST)
        theme.save()
        success = theme.success
        error_message = theme.error_message
        return load_view('cms', 'theme/update', theme = theme,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        theme = Theme.find(id)
        return load_view('cms', 'theme/trash', theme = theme,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        theme = Theme.find(id)
        theme.trash()
        success = theme.success
        error_message = theme.error_message
        return load_view('cms', 'theme/remove', theme = theme,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        theme = Theme.find(id)
        return load_view('cms', 'theme/delete', theme = theme,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        theme = Theme.find(id)
        theme.delete()
        success = theme.success
        error_message = theme.error_message
        return load_view('cms', 'theme/destroy', theme = theme,
            url_list = url_list, success = success, error_message = error_message)