from kokoropy import Autoroute_Controller, load_view, base_url, request

class Index_Controller(Autoroute_Controller):
    def action_index(self):
        url_list = {
            'Country' : base_url('country/country'),
            'Commodity' : base_url('country/commodity'),
            'City' : base_url('country/city'),
            'Political View' : base_url('country/political_view')
        }
        return load_view('country', 'index', url_list = url_list)