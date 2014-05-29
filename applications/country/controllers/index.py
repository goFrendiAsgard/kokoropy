from kokoropy import Autoroute_Controller, load_view, base_url, request

class Index_Controller(Autoroute_Controller):
    def action_index(self):
        url_list = {
            'City' : base_url('country/city/index'),
            'Political View' : base_url('country/political_view/index'),
            'Commodity' : base_url('country/commodity/index'),
            'Country' : base_url('country/country/index')
        }
        return load_view('country', 'index', url_list = url_list)