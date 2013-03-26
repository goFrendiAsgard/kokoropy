from kokoropy.bottle import template, request, route

## RECOMMENDED APPROACH (Automagically route) ############################################
#
# An OOP Style with automatic routing example (just like CodeIgniter or FuelPHP)
# The routing will be done automatically.
# To use this feature:
#    * The controller file name can be anything, and will be used for routing
#    * Your controller class name should be "Default_Controller"
#    * Your published method should have "action" prefix
#    * The published URL would be 
#      http://localhost:8080/app_dir/controller_file/published_method/params
#    * If your app_dir, controller_file or published_method named "index", it can be
#      omitted
#    * For convention, this is the recommended way to do it
##########################################################################################

class Default_Controller(object):
    # load the model
    def __init__(self):
        from application.example.models.simple_model import Simple_Model
        self.model = Simple_Model()
    
    # automatically routed to http://localhost:8080/
    def action(self):
        return template('example/hello', message='Automatic route working !!!', first_time=True)
    
    # automatically routed to: http://localhost:8080/auto/parameter
    def action_auto(self, name=None):
        message = self.model.say_hello(name)
        return template('example/hello', message='Automatically say '+message)
    
    # not routed
    def unpublished_function(self):
        return 'this is not published'