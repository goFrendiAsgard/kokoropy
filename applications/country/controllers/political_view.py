from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.country import City, Political_View, Commodity, Country, Rel_Country_Friends, Rel_Country_Commodities, Rel_Country_Enemies
import math

url_list = {
        'index'   : base_url('country/political_view/index'),
        'list'    : base_url('country/political_view/list'),
        'show'    : base_url('country/political_view/show'),
        'new'     : base_url('country/political_view/new'),
        'create'  : base_url('country/political_view/create'),
        'edit'    : base_url('country/political_view/edit'),
        'update'  : base_url('country/political_view/update'),
        'trash'   : base_url('country/political_view/trash'),
        'remove'  : base_url('country/political_view/remove'),
        'delete'  : base_url('country/political_view/delete'),
        'destroy' : base_url('country/political_view/destroy')
    }

class Political_View_Controller(Autoroute_Controller):
    
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
        political_view_list = Political_View.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Political_View.count())/limit))
        return load_view('country', 'political_view_list', 
            political_view_list = political_view_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        political_view = Political_View.find(id)
        political_view.set_state_show()
        return load_view('country', 'political_view_show', political_view = political_view,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        political_view = Political_View()
        political_view.set_state_insert()
        return load_view('country', 'political_view_new', political_view = political_view, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        political_view = Political_View()
        political_view.set_state_insert()
        # put your code here
        political_view.assign_from_dict(request.POST)
        political_view.save()
        success = political_view.success
        error_message = political_view.error_message
        return load_view('country', 'political_view_create', political_view = political_view,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        political_view = Political_View.find(id)
        political_view.set_state_update()
        return load_view('country', 'political_view_edit', political_view = political_view,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        political_view = Political_View.find(id)
        political_view.set_state_update()
        # put your code here
        political_view.assign_from_dict(request.POST)
        political_view.save()
        success = political_view.success
        error_message = political_view.error_message
        return load_view('country', 'political_view_update', political_view = political_view,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        political_view = Political_View.find(id)
        return load_view('country', 'political_view_trash', political_view = political_view,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        political_view = Political_View.find(id)
        political_view.trash()
        success = political_view.success
        error_message = political_view.error_message
        return load_view('country', 'political_view_remove', political_view = political_view,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        political_view = Political_View.find(id)
        return load_view('country', 'political_view_delete', political_view = political_view,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        political_view = Political_View.find(id)
        political_view.delete()
        success = political_view.success
        error_message = political_view.error_message
        return load_view('country', 'political_view_create', political_view = political_view,
            url_list = url_list, success = success, error_message = error_message)