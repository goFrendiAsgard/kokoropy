from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.auth import Third_Party, Group, Rel_User_Groups, User, Third_Party_Id
import math

url_list = {
        'index'   : base_url('cms/user/index'),
        'list'    : base_url('cms/user/list'),
        'show'    : base_url('cms/user/show'),
        'new'     : base_url('cms/user/new'),
        'create'  : base_url('cms/user/create'),
        'edit'    : base_url('cms/user/edit'),
        'update'  : base_url('cms/user/update'),
        'trash'   : base_url('cms/user/trash'),
        'remove'  : base_url('cms/user/remove'),
        'delete'  : base_url('cms/user/delete'),
        'destroy' : base_url('cms/user/destroy')
    }

class User_Controller(Autoroute_Controller):
    
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
        user_list = User.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(User.count())/limit))
        return load_view('cms', 'user_list', 
            user_list = user_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        user = User.find(id)
        return load_view('cms', 'user_show', user = user,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        user = User()
        return load_view('cms', 'user_new', user = user, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        user = User()
        # put your code here
        user.assign(request.POST)
        user.save()
        success = user.success
        error_message = user.error_message
        return load_view('cms', 'user_create', user = user,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        user = User.find(id)
        return load_view('cms', 'user_edit', user = user,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        user = User.find(id)
        # put your code here
        user.assign(request.POST)
        user.save()
        success = user.success
        error_message = user.error_message
        return load_view('cms', 'user_update', user = user,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        user = User.find(id)
        return load_view('cms', 'user_trash', user = user,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        user = User.find(id)
        user.trash()
        success = user.success
        error_message = user.error_message
        return load_view('cms', 'user_remove', user = user,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        user = User.find(id)
        return load_view('cms', 'user_delete', user = user,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        user = User.find(id)
        user.delete()
        success = user.success
        error_message = user.error_message
        return load_view('cms', 'user_create', user = user,
            url_list = url_list, success = success, error_message = error_message)