from kokoropy import template, route, request, base_url

class Hello_Controller(object):
    """
    Sample of advance route controller.
    After declaring the controller class, you need to define manual routing.
    """
    
    # load the model
    def __init__(self):
        from applications.example.models.simple_model import Simple_Model
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
        return template('example/views/advance_hello', message=message)

# make a Hello_Controller instance and define the manual routing
hello_controller = Hello_Controller()
route(base_url("/example/advance/hello"))(hello_controller.hello)
route(base_url("/example/advance/hello/"))(hello_controller.hello)
route(base_url("/example/advance/hello/<name>"))(hello_controller.hello)
route(base_url("/example/advance/hello/<name>/"))(hello_controller.hello)