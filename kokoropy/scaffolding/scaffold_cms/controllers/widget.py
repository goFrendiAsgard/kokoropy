from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.cms import Widget, User_Third_Party_Identities, Group, Language_Detail, Language, Third_Party_Authenticator, Theme, User, Configuration, Page_Groups, Layout, User_Groups, Cms, Page, Widget_Groups
import math

url_list = {
        'index'   : base_url('cms/widget/index'),
        'list'    : base_url('cms/widget/list'),
        'show'    : base_url('cms/widget/show'),
        'new'     : base_url('cms/widget/new'),
        'create'  : base_url('cms/widget/create'),
        'edit'    : base_url('cms/widget/edit'),
        'update'  : base_url('cms/widget/update'),
        'trash'   : base_url('cms/widget/trash'),
        'remove'  : base_url('cms/widget/remove'),
        'delete'  : base_url('cms/widget/delete'),
        'destroy' : base_url('cms/widget/destroy')
    }

class Widget_Controller(Autoroute_Controller):
    
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
        widget_list = Widget.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Widget.count())/limit))
        return load_view('cms', 'widget/list', 
            widget_list = widget_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        widget = Widget.find(id)
        widget.set_state_show()
        return load_view('cms', 'widget/show', widget = widget,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        widget = Widget()
        widget.set_state_insert()
        return load_view('cms', 'widget/new', widget = widget, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        widget = Widget()
        widget.set_state_insert()
        # put your code here
        widget.assign_from_dict(request.POST)
        widget.save()
        success = widget.success
        error_message = widget.error_message
        return load_view('cms', 'widget/create', widget = widget,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        widget = Widget.find(id)
        widget.set_state_update()
        return load_view('cms', 'widget/edit', widget = widget,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        widget = Widget.find(id)
        widget.set_state_update()
        # put your code here
        widget.assign_from_dict(request.POST)
        widget.save()
        success = widget.success
        error_message = widget.error_message
        return load_view('cms', 'widget/update', widget = widget,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        widget = Widget.find(id)
        return load_view('cms', 'widget/trash', widget = widget,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        widget = Widget.find(id)
        widget.trash()
        success = widget.success
        error_message = widget.error_message
        return load_view('cms', 'widget/remove', widget = widget,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        widget = Widget.find(id)
        return load_view('cms', 'widget/delete', widget = widget,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        widget = Widget.find(id)
        widget.delete()
        success = widget.success
        error_message = widget.error_message
        return load_view('cms', 'widget/destroy', widget = widget,
            url_list = url_list, success = success, error_message = error_message)