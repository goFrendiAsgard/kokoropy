from kokoropy import template, route, request, base_url, load_model, load_view

class My_Controller(object):
    """
    Sample of advance route controller.
    After declaring the controller class, you need to define manual routing.
    """
    
    # load the model
    def __init__(self):
        Simple_Model = load_model('example', 'simple_model')
        self.simple_model = Simple_Model()
        
    def hello(self, name=None):
        # get counter from SESSION, or set it
        if 'counter' in request.SESSION:
            request.SESSION['counter'] += 1
        else:
            request.SESSION['counter'] = 1        
        # get say_hello
        say_hello = self.simple_model.say_hello(name)
        message = say_hello+', the session said that you have visit routing demo page '+str(request.SESSION['counter'])+' times'
        return load_view('example', 'advance_hello', message=message)