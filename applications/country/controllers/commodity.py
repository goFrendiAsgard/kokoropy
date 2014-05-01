from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.country import City, Political_View, Commodity, Country, Rel_Country_Friends, Rel_Country_Commodities, Rel_Country_Enemies

url_list = {
        'index'   : base_url('country/commodity/index'),
        'list'    : base_url('country/commodity/list'),
        'show'    : base_url('country/commodity/show'),
        'new'     : base_url('country/commodity/new'),
        'create'  : base_url('country/commodity/create'),
        'edit'    : base_url('country/commodity/edit'),
        'update'  : base_url('country/commodity/update'),
        'trash'   : base_url('country/commodity/trash'),
        'remove'  : base_url('country/commodity/remove'),
        'delete'  : base_url('country/commodity/delete'),
        'destroy' : base_url('country/commodity/destroy')
    }

class Commodity_Controller(Autoroute_Controller):
    
    def action_index(self):
        return self.action_list()
    
    def action_list(self):
        ''' Show table '''
        commodity_list = Commodity.get()
        return load_view('country', 'commodity_list', 
             commodity_list = commodity_list, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        commodity = Commodity.find(id)
        return load_view('country', 'commodity_show', commodity = commodity,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        commodity = Commodity()
        return load_view('country', 'commodity_new', commodity = commodity, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        commodity = Commodity()
        # put your code here
        commodity.assign(request.POST)
        commodity.save()
        success = commodity.success
        error_message = commodity.error_message
        return load_view('country', 'commodity_create', commodity = commodity,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        commodity = Commodity.find(id)
        return load_view('country', 'commodity_edit', commodity = commodity,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        commodity = Commodity.find(id)
        # put your code here
        commodity.assign(request.POST)
        commodity.save()
        success = commodity.success
        error_message = commodity.error_message
        return load_view('country', 'commodity_update', commodity = commodity,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        commodity = Commodity.find(id)
        return load_view('country', 'commodity_trash', commodity = commodity,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        commodity = Commodity.find(id)
        commodity.trash()
        success = commodity.success
        error_message = commodity.error_message
        return load_view('country', 'commodity_remove', commodity = commodity,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        commodity = Commodity.find(id)
        return load_view('country', 'commodity_delete', commodity = commodity,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        commodity = Commodity.find(id)
        commodity.delete()
        success = commodity.success
        error_message = commodity.error_message
        return load_view('country', 'commodity_create', commodity = commodity,
            url_list = url_list, success = success, error_message = error_message)