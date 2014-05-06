from kokoropy import Autoroute_Controller, load_view, base_url, request

class Index_Controller(Autoroute_Controller):
    def action_index(self):
        url_list = {
            # g_url_pairs
        }
        return load_view('g_application_name', 'index', url_list = url_list)