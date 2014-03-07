from kokoropy import Autoroute_Controller, load_view

class My_Controller(Autoroute_Controller):
    '''
    Example collections
    '''

    def action_index(self):
        return load_view('example', 'index')
