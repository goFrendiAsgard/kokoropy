from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/cms/index'),
        'list'    : base_url('cms/cms/list'),
        'show'    : base_url('cms/cms/show'),
        'new'     : base_url('cms/cms/new'),
        'create'  : base_url('cms/cms/create'),
        'edit'    : base_url('cms/cms/edit'),
        'update'  : base_url('cms/cms/update'),
        'trash'   : base_url('cms/cms/trash'),
        'remove'  : base_url('cms/cms/remove'),
        'delete'  : base_url('cms/cms/delete'),
        'destroy' : base_url('cms/cms/destroy')
    }

class Cms_Controller(Autoroute_Controller):
    
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
        cms_list = Cms.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Cms.count())/limit))
        return load_view('cms', 'cms/list', 
            cms_list = cms_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        cms = Cms.find(id)
        cms.set_state_show()
        return load_view('cms', 'cms/show', cms = cms,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        cms = Cms()
        cms.set_state_insert()
        return load_view('cms', 'cms/new', cms = cms, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        cms = Cms()
        cms.set_state_insert()
        # put your code here
        cms.assign_from_dict(request.POST)
        cms.save()
        success = cms.success
        error_message = cms.error_message
        return load_view('cms', 'cms/create', cms = cms,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        cms = Cms.find(id)
        cms.set_state_update()
        return load_view('cms', 'cms/edit', cms = cms,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        cms = Cms.find(id)
        cms.set_state_update()
        # put your code here
        cms.assign_from_dict(request.POST)
        cms.save()
        success = cms.success
        error_message = cms.error_message
        return load_view('cms', 'cms/update', cms = cms,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        cms = Cms.find(id)
        return load_view('cms', 'cms/trash', cms = cms,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        cms = Cms.find(id)
        cms.trash()
        success = cms.success
        error_message = cms.error_message
        return load_view('cms', 'cms/remove', cms = cms,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        cms = Cms.find(id)
        return load_view('cms', 'cms/delete', cms = cms,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        cms = Cms.find(id)
        cms.delete()
        success = cms.success
        error_message = cms.error_message
        return load_view('cms', 'cms/destroy', cms = cms,
            url_list = url_list, success = success, error_message = error_message)