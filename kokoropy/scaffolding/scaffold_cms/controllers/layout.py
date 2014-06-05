from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/layout/index'),
        'list'    : base_url('cms/layout/list'),
        'show'    : base_url('cms/layout/show'),
        'new'     : base_url('cms/layout/new'),
        'create'  : base_url('cms/layout/create'),
        'edit'    : base_url('cms/layout/edit'),
        'update'  : base_url('cms/layout/update'),
        'trash'   : base_url('cms/layout/trash'),
        'remove'  : base_url('cms/layout/remove'),
        'delete'  : base_url('cms/layout/delete'),
        'destroy' : base_url('cms/layout/destroy')
    }

class Layout_Controller(Autoroute_Controller):
    
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
        layout_list = Layout.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Layout.count())/limit))
        return load_view('cms', 'layout/list', 
            layout_list = layout_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        layout = Layout.find(id)
        layout.set_state_show()
        return load_view('cms', 'layout/show', layout = layout,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        layout = Layout()
        layout.set_state_insert()
        return load_view('cms', 'layout/new', layout = layout, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        layout = Layout()
        layout.set_state_insert()
        # put your code here
        layout.assign_from_dict(request.POST)
        layout.save()
        success = layout.success
        error_message = layout.error_message
        return load_view('cms', 'layout/create', layout = layout,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        layout = Layout.find(id)
        layout.set_state_update()
        return load_view('cms', 'layout/edit', layout = layout,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        layout = Layout.find(id)
        layout.set_state_update()
        # put your code here
        layout.assign_from_dict(request.POST)
        layout.save()
        success = layout.success
        error_message = layout.error_message
        return load_view('cms', 'layout/update', layout = layout,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        layout = Layout.find(id)
        return load_view('cms', 'layout/trash', layout = layout,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        layout = Layout.find(id)
        layout.trash()
        success = layout.success
        error_message = layout.error_message
        return load_view('cms', 'layout/remove', layout = layout,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        layout = Layout.find(id)
        return load_view('cms', 'layout/delete', layout = layout,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        layout = Layout.find(id)
        layout.delete()
        success = layout.success
        error_message = layout.error_message
        return load_view('cms', 'layout/destroy', layout = layout,
            url_list = url_list, success = success, error_message = error_message)