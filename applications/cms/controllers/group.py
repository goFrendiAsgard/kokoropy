from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.auth import Rel_Page_Groups, Group, Page
import math

url_list = {
        'index'   : base_url('cms/group/index'),
        'list'    : base_url('cms/group/list'),
        'show'    : base_url('cms/group/show'),
        'new'     : base_url('cms/group/new'),
        'create'  : base_url('cms/group/create'),
        'edit'    : base_url('cms/group/edit'),
        'update'  : base_url('cms/group/update'),
        'trash'   : base_url('cms/group/trash'),
        'remove'  : base_url('cms/group/remove'),
        'delete'  : base_url('cms/group/delete'),
        'destroy' : base_url('cms/group/destroy')
    }

class Group_Controller(Autoroute_Controller):
    
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
        group_list = Group.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Group.count())/limit))
        return load_view('cms', 'group_list', 
            group_list = group_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        group = Group.find(id)
        return load_view('cms', 'group_show', group = group,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        group = Group()
        return load_view('cms', 'group_new', group = group, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        group = Group()
        # put your code here
        group.assign(request.POST)
        group.save()
        success = group.success
        error_message = group.error_message
        return load_view('cms', 'group_create', group = group,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        group = Group.find(id)
        return load_view('cms', 'group_edit', group = group,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        group = Group.find(id)
        # put your code here
        group.assign(request.POST)
        group.save()
        success = group.success
        error_message = group.error_message
        return load_view('cms', 'group_update', group = group,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        group = Group.find(id)
        return load_view('cms', 'group_trash', group = group,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        group = Group.find(id)
        group.trash()
        success = group.success
        error_message = group.error_message
        return load_view('cms', 'group_remove', group = group,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        group = Group.find(id)
        return load_view('cms', 'group_delete', group = group,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        group = Group.find(id)
        group.delete()
        success = group.success
        error_message = group.error_message
        return load_view('cms', 'group_create', group = group,
            url_list = url_list, success = success, error_message = error_message)