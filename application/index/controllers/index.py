from application import app
from kokoropy.bottle import template, request

## APPROACH 1 (Simple but deadly works) ##################################################
#
# A very simple procedural style example
# Manually routed to http://localhost:8080/ with @app.route decorator
##########################################################################################

@app.route('/hello_world')
def index():
    return 'Hello world, I am alive !!!<br /><a href="/">Now go back to work</a>'


## APPROACH 2 (Automagically route) ######################################################
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
        from application.index.models.example_model import Hello_Model
        self.model = Hello_Model()
    
    # automatically routed to http://localhost:8080/
    def action(self):
        return template('example/hello', message='Automatic route working !!!')
    
    # automatically routed to: http://localhost:8080/auto/parameter
    def action_auto(self, name=None):
        message = self.model.say_hello(name)
        return template('example/hello', message='Automatically say '+message)
    
    # not routed
    def unpublished_function(self):
        return 'this is not published'



## APPROACH 3 (Your route, your style, your freedom) #####################################
#
# An OOP style with user defined routing example
# After declaring the controller class, you need to define manual routing
##########################################################################################

class Hello_Controller(object):
    
    # load the model
    def __init__(self):
        from application.index.models.example_model import Hello_Model
        self.model = Hello_Model()
    
    # will be manually routed to http://localhost/hello
    def hello_param(self, name = None):
        message = self.model.say_hello(name)
        return template('example/hello', message=message)
    
    def hello_get(self):
        ##################################################################################
        # Python                            #  equivalent PHP code                       #
        ##################################################################################
        name = None                         # $name = NULL;                              #
        if 'name' in request.GET:           # if(isset($_GET['name']))                   #
            name = request.GET['name']      #    $name = $_GET['name'];                  #
        ##################################################################################
        message = self.model.say_hello(name)
        return template('example/hello', message=message)
    
    def pokemon(self):
        pokemons = self.model.get_pokemon()
        return template('example/pokemon', pokemons=pokemons)

# make a Hello_Controller instance
my_controller = Hello_Controller()
app.route("/hello", method='GET')(my_controller.hello_get)
app.route("/hello/<name>")(my_controller.hello_param)
app.route("/pokemon")(my_controller.pokemon)