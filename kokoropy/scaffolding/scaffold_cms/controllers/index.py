from kokoropy import Autoroute_Controller, load_view, base_url, request

class Index_Controller(Autoroute_Controller):
    def action_index(self):
        url_list = {
            'Cms' : base_url('cms/cms/index'),
            'Group' : base_url('cms/group/index'),
            'Third Party Authenticator' : base_url('cms/third_party_authenticator/index'),
            'Page' : base_url('cms/page/index'),
            'Theme' : base_url('cms/theme/index'),
            'Layout' : base_url('cms/layout/index'),
            'Widget' : base_url('cms/widget/index'),
            'User' : base_url('cms/user/index'),
            'Language' : base_url('cms/language/index'),
            'Language Detail' : base_url('cms/language_detail/index'),
            'Configuration' : base_url('cms/configuration/index')
        }
        return load_view('cms', 'index', url_list = url_list)