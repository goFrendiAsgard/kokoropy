from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.country import City, Political_View, Commodity, Country, Rel_Country_Friends, Rel_Country_Commodities, Rel_Country_Enemies
import math

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
        # get page index
        current_page = int(request.GET['page']) if 'page' in request.GET else 1
        # determine limit and offset
        limit = 50
        offset = (current_page-1) * limit
        # get the data
        city_list = City.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(City.count())/limit))
        return load_view('country', 'city_list', 
            city_list = city_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        city = City.find(id)
        city.set_state_show()
        return load_view('country', 'city_show', city = city,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        city = City()
        city.set_state_insert()
        return load_view('country', 'city_new', city = city, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        city = City()
        city.set_state_insert()
        # put your code here
        city.assign_from_dict(request.POST)
        city.save()
        success = city.success
        error_message = city.error_message
        return load_view('country', 'city_create', city = city,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        city = City.find(id)
        city.set_state_update()
        return load_view('country', 'city_edit', city = city,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        city = City.find(id)
        city.set_state_update()
        # put your code here
        city.assign_from_dict(request.POST)
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