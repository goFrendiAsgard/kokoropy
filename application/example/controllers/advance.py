from kokoropy.bottle import template, request, route

## ADVANCE APPROACH (Your route, your style, your freedom) ###############################
#
# An OOP style with user defined routing example
# After declaring the controller class, you need to define manual routing
##########################################################################################

class Hello_Controller(object):
    
    # load the model
    def __init__(self):
        from application.example.models.simple_model import Simple_Model
        from application.example.models.db_model import DB_Model
        self.simple_model = Simple_Model()
        self.db_model = DB_Model()
    
    # will be manually routed to http://localhost/example/advance/hello
    def hello_param(self, name = None):
        message = self.simple_model.say_hello(name)
        return template('example/hello', message=message)
    
    # will be manually routed to http://localhost/example/advance/hello/param
    def hello_get(self):
        ##################################################################################
        # Python                            #  equivalent PHP code                       #
        ##################################################################################
        name = None                         # $name = NULL;                              #
        if 'name' in request.GET:           # if(isset($_GET['name']))                   #
            name = request.GET['name']      #    $name = $_GET['name'];                  #
        ##################################################################################
        message = self.simple_model.say_hello(name)
        return template('example/hello', message=message)
    
    # will be manually routed to http://localhost/advance/pokemon
    def pokemon(self):
        pokemons = self.db_model.get_pokemon()
        return template('example/pokemon', pokemons=pokemons)

# make a Hello_Controller instance and define the routing
hello_controller = Hello_Controller()
route("/example/advance/hello", method='GET')(hello_controller.hello_get)
route("/example/advance/hello/<name>")(hello_controller.hello_param)
route("/example/advance/pokemon")(hello_controller.pokemon)