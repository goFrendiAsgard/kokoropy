from application import app
from kokoropy.bottle import template, request

#########################################################################
# A very simple procedural style example
#########################################################################
@app.route('/', method='GET')
def index():
    return 'Hello world, I am alive !!!<br /><a href="/hello">See what I can do now</a>'


#########################################################################
# An OOP style example
#########################################################################

# Hello_Controller's class definition
class Hello_Controller(object):
    def __init__(self):
        # import Hello_Model
        from application.example.models.example_model import Hello_Model
        # make an instance of Hello_Model, 
        # make it as Hello_Controller's property        
        self.model = Hello_Model()
        
    def hello_normal(self, name = None):
        # get value returned by model.say_hello
        message = self.model.say_hello(name)
        # render it by using example/hello.tpl template
        return template('example/hello', message=message)
    
    def hello_get(self):
        #######################################################################
        # get URL query parameter                                             #
        # (e.g: http://localhost:8080/hello?name=Haruna)                      #
        # if you want to catch POST request, you can use request.POST         #
        # I also give PHP equivalent code as comment:                         #
        #######################################################################
        # Python                            # PHP                             #
        #######################################################################
        name = None                         # $name = NULL;                   #
        if 'name' in request.GET:           # if(isset($_GET['name']))        #
            name = request.GET['name']      #    $name = $_GET['name'];       #
        #######################################################################        
        # get value returned by model.say_hello
        message = self.model.say_hello(name)
        # render it by using example/hello.tpl template
        return template('example/hello', message=message)
    
    def pokemon(self):
        pokemons = self.model.get_pokemon()
        return template('example/pokemon', pokemons=pokemons)

# make a Hello_Controller instance
my_controller = Hello_Controller()

# route to class method
app.route("/hello", method='GET')(my_controller.hello_get)
app.route("/hello/<name>")(my_controller.hello_normal)
app.route("/pokemon")(my_controller.pokemon)