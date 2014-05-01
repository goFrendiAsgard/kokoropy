from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.country import City, Political_View, Commodity, Country, Rel_Country_Friends, Rel_Country_Commodities, Rel_Country_Enemies

url_list = {
        'index'   : base_url('country/city/index'),
        'list'    : base_url('country/city/list'),
        'show'    : base_url('country/city/show'),
        'new'     : base_url('country/city/new'),
        'create'  : base_url('country/city/create'),
        'edit'    : base_url('country/city/edit'),
        'update'  : base_url('country/city/update'),
        'trash'   : base_url('country/city/trash'),
        'remove'  : base_url('country/city/remove'),
        'delete'  : base_url('country/city/delete'),
        'destroy' : base_url('country/city/destroy')
    }

class City_Controller(Autoroute_Controller):
    
    def action_index(self):
        return self.action_list()
    
    def action_list(self):
        ''' Show table '''
        city_list = City.get()
        return load_view('country', 'city_list', 
             city_list = city_list, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        city = City.find(id)
        return load_view('country', 'city_show', city = city,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        city = City()
        return load_view('country', 'city_new', city = city, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        city = City()
        # put your code here
        city.assign(request.POST)
        city.save()
        success = city.success
        error_message = city.error_message
        return load_view('country', 'city_create', city = city,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        city = City.find(id)
        return load_view('country', 'city_edit', city = city,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        city = City.find(id)
        # put your code here
        city.assign(request.POST)
        city.save()
        success = city.success
        error_message = city.error_message
        return load_view('country', 'city_update', city = city,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        city = City.find(id)
        return load_view('country', 'city_trash', city = city,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        city = City.find(id)
        city.trash()
        success = city.success
        error_message = city.error_message
        return load_view('country', 'city_remove', city = city,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        city = City.find(id)
        return load_view('country', 'city_delete', city = city,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        city = City.find(id)
        city.delete()
        success = city.success
        error_message = city.error_message
        return load_view('country', 'city_create', city = city,
            url_list = url_list, success = success, error_message = error_message)