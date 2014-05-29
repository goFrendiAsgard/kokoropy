from kokoropy import Autoroute_Controller, load_view, base_url, request
from ..models.country import City, Political_View, Commodity, Country, Rel_Country_Friends, Rel_Country_Commodities, Rel_Country_Enemies
import math

url_list = {
        'index'   : base_url('country/country/index'),
        'list'    : base_url('country/country/list'),
        'show'    : base_url('country/country/show'),
        'new'     : base_url('country/country/new'),
        'create'  : base_url('country/country/create'),
        'edit'    : base_url('country/country/edit'),
        'update'  : base_url('country/country/update'),
        'trash'   : base_url('country/country/trash'),
        'remove'  : base_url('country/country/remove'),
        'delete'  : base_url('country/country/delete'),
        'destroy' : base_url('country/country/destroy')
    }

class Country_Controller(Autoroute_Controller):
    
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
        country_list = Country.get(limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(Country.count())/limit))
        return load_view('country', 'country_list', 
            country_list = country_list, current_page = current_page,
            page_count = page_count, url_list = url_list)
    
    def action_show(self, id):
        ''' Show One Record '''
        country = Country.find(id)
        country.set_state_show()
        return load_view('country', 'country_show', country = country,
            url_list = url_list)
    
    def action_new(self):
        ''' Insert Form '''
        country = Country()
        country.set_state_insert()
        return load_view('country', 'country_new', country = country, 
            url_list = url_list)
    
    def action_create(self):
        ''' Insert Action '''
        country = Country()
        country.set_state_insert()
        # put your code here
        country.assign_from_dict(request.POST)
        country.save()
        success = country.success
        error_message = country.error_message
        return load_view('country', 'country_create', country = country,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_edit(self, id):
        ''' Update Form '''
        country = Country.find(id)
        country.set_state_update()
        return load_view('country', 'country_edit', country = country,
            url_list = url_list)
    
    def action_update(self,id):
        ''' Update Action '''
        country = Country.find(id)
        country.set_state_update()
        # put your code here
        country.assign_from_dict(request.POST)
        country.save()
        success = country.success
        error_message = country.error_message
        return load_view('country', 'country_update', country = country,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_trash(self, id):
        ''' Trash Form '''
        country = Country.find(id)
        return load_view('country', 'country_trash', country = country,
            url_list = url_list)
    
    def action_remove(self, id):
        ''' Trash Action '''
        country = Country.find(id)
        country.trash()
        success = country.success
        error_message = country.error_message
        return load_view('country', 'country_remove', country = country,
            url_list = url_list, success = success, error_message = error_message)
    
    def action_delete(self, id):
        ''' Delete Form '''
        country = Country.find(id)
        return load_view('country', 'country_delete', country = country,
            url_list = url_list)
    
    def action_destroy(self, id):
        ''' Delete Action '''
        country = Country.find(id)
        country.delete()
        success = country.success
        error_message = country.error_message
        return load_view('country', 'country_create', country = country,
            url_list = url_list, success = success, error_message = error_message)