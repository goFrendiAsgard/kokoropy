from kokoropy import Autoroute_Controller, load_view, base_url, request

class Index_Controller(Autoroute_Controller):
    def action_index(self):
        url_list = {
            'Group' : base_url('cms/group'),
            'Third Party Authenticator' : base_url('cms/third_party_authenticator'),
            'Page' : base_url('cms/page'),
            'Theme' : base_url('cms/theme'),
            'Layout' : base_url('cms/layout'),
            'Widget' : base_url('cms/widget'),
            'User' : base_url('cms/user'),
            'Language' : base_url('cms/language'),
            'Configuration' : base_url('cms/configuration')
        }
        return load_view('cms', 'index', url_list = url_list)