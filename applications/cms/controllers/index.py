from kokoropy import Autoroute_Controller, load_view, base_url, request

class Index_Controller(Autoroute_Controller):
    def action_index(self):
        url_list = {
            'Third Party' : base_url('cms/third_party/index'),
            'Group' : base_url('cms/group/index'),
            'User' : base_url('cms/user/index'),
            'Page' : base_url('cms/page/index')
        }
        return load_view('cms', 'index', url_list = url_list)