from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.auth import Rel_Page_Groups, Group, Page
import math

url_list = {
        'index'   : base_url('cms/page/index'),
        'list'    : base_url('cms/page/list'),
        'show'    : base_url('cms/page/show'),
        'new'     : base_url('cms/page/new'),
        'create'  : base_url('cms/page/create'),
        'edit'    : base_url('cms/page/edit'),
        'update'  : base_url('cms/page/update'),
        'trash'   : base_url('cms/page/trash'),
        'remove'  : base_url('cms/page/remove'),
        'delete'  : base_url('cms/page/delete'),
        'destroy' : base_url('cms/page/destroy')
    }

class Page_Controller(Autoroute_Controller):
    
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
        page_list = Page.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Page.count())/limit))
        return load_view('cms', 'page_list', 
            page_list = page_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        page = Page.find(id)
        return load_view('cms', 'page_show', page = page,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        page = Page()
        return load_view('cms', 'page_new', page = page, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        page = Page()
        # put your code here
        page.assign_from_dict(request.POST)
        page.save()
        success = page.success
        error_message = page.error_message
        return load_view('cms', 'page_create', page = page,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        page = Page.find(id)
        return load_view('cms', 'page_edit', page = page,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        page = Page.find(id)
        # put your code here
        page.assign_from_dict(request.POST)
        page.save()
        success = page.success
        error_message = page.error_message
        return load_view('cms', 'page_update', page = page,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        page = Page.find(id)
        return load_view('cms', 'page_trash', page = page,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        page = Page.find(id)
        page.trash()
        success = page.success
        error_message = page.error_message
        return load_view('cms', 'page_remove', page = page,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        page = Page.find(id)
        return load_view('cms', 'page_delete', page = page,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        page = Page.find(id)
        page.delete()
        success = page.success
        error_message = page.error_message
        return load_view('cms', 'page_create', page = page,
            url_list = url_list, success = success, error_message = error_message)