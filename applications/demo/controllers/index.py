from kokoropy import Autoroute_Controller, load_view, base_url, request

class Index_Controller(Autoroute_Controller):
    def action_index(self):
        url_list = {
            'Village' : base_url('demo/village'),
            'Clan' : base_url('demo/clan'),
            'Resource' : base_url('demo/resource')
        }
        return load_view('demo', 'index', url_list = url_list)