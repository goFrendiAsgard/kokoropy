Kokoropy
=========

A MVC python web framework, from my heart <3

In japanese, kokoro means heart
I make kokoropy because I can't find any python web-framework which I really comfort with.

This is my pet-project, and might be not stable. Don't use it for production purpose !!!

Kokoropy is built based on my experiences with some framework. Here are some comparison between kokoropy and other framework

* In kokoropy, controller name doesn't correspond to URL
* kokoropy is explicit. There is no such a "magic" like in web2py
* You can use route directive in bottle.py, since bottle.py is the core of kokoropy
* kokoropy is built based on HMVC pattern, like laravel, fuelPHP and CodeIgniter+HMVC
* kokoropy doesn't have any other dependencies. You can even run it without Apache or nginx
* kokoropy has a funny dragon guarding important source codes, just as laravel :)

How to use
==========

First, you need to create a python package in application folder. The package should consist of

* "controllers" subpackage
* "models" subpackage
* "views" directory
* "static" directory

Inside the controllers subpackage, create a python file (name is not important, it is not PHP)
The routing is done via route directive.
Create something like this:

```python
    from application import app
    
    @app.route('/', method='GET')
    def index():
        return "Hello world"
```

Open start.py, edit configuration. Be careful, there is a dragon there.
Modify some key configuration or leave it as is

```python
    HOST                = 'localhost'
    PORT                = 8080
    DEBUG               = True
    RELOADER            = True
```

Open your console, and do this:

```
    python start.py
```

Open your browser, access the page

```
   http://localhost:8080/ 
```

MVC
===

MVC stands for "Model-View-Controller". Almost all modern web framework use such a mechanism. 
In kokoropy, You can have several MVC triad located at /application

Model
-----
Model is the heart of your application. 
It is not necessarily required, but definitely recommended.
Model should define what your application can do.
Using OOP approach will make your model looks more elegant, but don't worry, procedural style is still okay.
Unlike java, your class name can be different from your file name. Here you have freedom.

kokoropy come with a basic example model located at /application/example/models/example_model.py

```python
    class Hello_Model(object):
        
        def say_hello(self, name=None):
            if name is None:
                return "Hello Stranger"
            else:
                return "Hello "+name
        
        def get_pokemon(self):
            return ['bubasaur', 'charmender', 'squirtle', 'caterpie', 'pikachu']
```

This model can say hello, and can give you a lit of pokemons


Controller
----------
Have a model, make your application able to do things, but have a controller let you do things
Controller is a gateway into your model. Of course, putting some logic here is possible.
Just keep in mind to keep your controller as slim as possible.

kokoropy come with a basic example controller located at /application/example/controllers/index.py

```python
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
```
Using procedural style, you can define your routing with @app.route() decorator
Using OOP style, you can use app.route()

View
----
It is wise to not put presentation logic in your controller.

You can separate your view into several template.
Let's say you have a baste template at /application/example/views/base.tpl

```html
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/example/css/style.css" />
        <title>{{ title or 'Kokoropy' }}</title>
    </head>
    <body>
        <h1>Kokoro py</h1>
        <h2>A pythonic MVC Web Framework</h2>
        <p id="links">
            <a href="/hello">A normal hello without parameter</a>
            <a href="/hello?name=Rina">Hello with query</a>
            <a href="/hello/Haruna">Hello with parameter</a>
            <a href="/pokemon">Pokemon</a>
        </p>
        <p id="content">
            %include
        </p>
        <footer>GoFrendiAsgard &copy; 2013<footer>
    </body>
    </html>
```

and another template at /application/example/views/pokemon.tpl

```html
    <strong>Pokemon list:</strong>
    <ul>
    %for pokemon in pokemons:
        <li>{{pokemon}}</li>
    %end
    </ul>
    %rebase example/base title='Pokemon'
````

pokemon.tpl will include base.tpl and override %include.
As you see, you can also put some (limitted) python script in the template
