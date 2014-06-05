from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/configuration/index'),
        'list'    : base_url('cms/configuration/list'),
        'show'    : base_url('cms/configuration/show'),
        'new'     : base_url('cms/configuration/new'),
        'create'  : base_url('cms/configuration/create'),
        'edit'    : base_url('cms/configuration/edit'),
        'update'  : base_url('cms/configuration/update'),
        'trash'   : base_url('cms/configuration/trash'),
        'remove'  : base_url('cms/configuration/remove'),
        'delete'  : base_url('cms/configuration/delete'),
        'destroy' : base_url('cms/configuration/destroy')
    }

class Configuration_Controller(Autoroute_Controller):
    
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
        configuration_list = Configuration.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Configuration.count())/limit))
        return load_view('cms', 'configuration/list', 
            configuration_list = configuration_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        configuration = Configuration.find(id)
        configuration.set_state_show()
        return load_view('cms', 'configuration/show', configuration = configuration,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        configuration = Configuration()
        configuration.set_state_insert()
        return load_view('cms', 'configuration/new', configuration = configuration, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        configuration = Configuration()
        configuration.set_state_insert()
        # put your code here
        configuration.assign_from_dict(request.POST)
        configuration.save()
        success = configuration.success
        error_message = configuration.error_message
        return load_view('cms', 'configuration/create', configuration = configuration,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        configuration = Configuration.find(id)
        configuration.set_state_update()
        return load_view('cms', 'configuration/edit', configuration = configuration,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        configuration = Configuration.find(id)
        configuration.set_state_update()
        # put your code here
        configuration.assign_from_dict(request.POST)
        configuration.save()
        success = configuration.success
        error_message = configuration.error_message
        return load_view('cms', 'configuration/update', configuration = configuration,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        configuration = Configuration.find(id)
        return load_view('cms', 'configuration/trash', configuration = configuration,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        configuration = Configuration.find(id)
        configuration.trash()
        success = configuration.success
        error_message = configuration.error_message
        return load_view('cms', 'configuration/remove', configuration = configuration,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        configuration = Configuration.find(id)
        return load_view('cms', 'configuration/delete', configuration = configuration,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        configuration = Configuration.find(id)
        configuration.delete()
        success = configuration.success
        error_message = configuration.error_message
        return load_view('cms', 'configuration/destroy', configuration = configuration,
            url_list = url_list, success = success, error_message = error_message)