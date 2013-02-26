Kokoropy
=========

A MVC python web framework, from my heart <3

In japanese, kokoro means heart
I make kokoropy because I can't find any python web-framework which I really comfort with.
Some are too verbose, while some other are to "magic". Most of them force me to learn about the framework, and not allow me to focus on my job.
Basically I expect an easy framework like CodeIgniter (of course, with more features) in python.

If you are in the same boat with me, then kokoropy is for you.

Kokoropy is built in top of Bottle.py (http://bottlepy.org/docs/dev/), a very great python micro-framework.
While bottle.py focus on how to make things as simple as possible, kokoropy focus on how to make things as easy as possible.
If you've once ever use my another open source project, No-CMS (http://getnocms.com), you will know what I mean by easy.

Kokoropy is built based on my experiences with some framework. Here are some comparison between kokoropy and other framework

* In kokoropy, controller name doesn't correspond to URL
* kokoropy is explicit. There is no such a "magic" like in web2py
* You can use route directive in bottle.py, since bottle.py is the core of kokoropy. 
* kokoropy is built based on HMVC pattern, like laravel, fuelPHP and CodeIgniter+HMVC
* kokoropy doesn't have any other dependencies. You can even run it without Apache or nginx
* kokoropy has a funny dragon guarding important source codes, just as laravel :)

__PS:__ This is my pet-project, and might be not stable. It is not ready for production purpose (yet)

How to use
==========

First, you need to create a python package in application folder. The package should consist of

* "controllers" subpackage
* "models" subpackage
* "views" directory
* "static" directory

__PS:__ To understand about package in python, please visit http://docs.python.org/2/tutorial/modules.html#packages

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

Unlike PHP, you don't need to worry about error message. Every error message will be shown in console, not in browser

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

This model can say hello, and can give you a list of pokemons


Controller
----------
Have a model, make your application able to do things, but have a controller let you do things.
Controller is a gateway into your model. Of course, putting some logic here is possible.
Just keep in mind to keep your controller as slim as possible.

kokoropy come with a basic example controller located at /application/example/controllers/index.py

```python
    from application import app
    from kokoropy.bottle import template, request
    
    ##########################################################################################
    # A very simple procedural style example
    # You can say hello world in just 3 lines
    ##########################################################################################
    
    # http://localhost:8080/
    @app.route('/', method='GET')
    def index():
        return 'Hello world, I am alive !!!<br /><a href="/hello">See what I can do now</a>'
    
    
    ##########################################################################################
    # An OOP Style with automatic routing example (just like CodeIgniter)
    # To have an automatic routing, your controller class name should be 'Default_Controller'
    # You cannot do automatic routing by using procedural approach
    ##########################################################################################
    
    class Default_Controller(object):
        
        # http://localhost:8080/example/
        def action(self):
            return 'This is the default action'
        
        # http://localhost:8080/example/index/auto
        # http://localhost:8080/example/index/auto/parameter
        # http://localhost:8080/example/auto
        # http://localhost:8080/example/auto/parameter
        def action_auto(self, param_1=None):
            if param_1 is None:
                param_1 = 'No value'
            return 'You have enter a parameter : '+param_1
        
        def unpublished_function(self):
            return 'this is not published'
    
    
    ##########################################################################################
    # An OOP style with user defined routing example
    # In case you don't like automatic routing, you are free to define your own.
    ##########################################################################################
    
    # Hello_Controller's class definition
    class Hello_Controller(object):
        def __init__(self):
            # import Hello_Model
            from application.example.models.example_model import Hello_Model
            # make an instance of Hello_Model, 
            # make it as Hello_Controller's property        
            self.model = Hello_Model()
        
        # Routing will be defined later
        # http://localhost:8080/hello/name
        def hello_param(self, name = None):
            # get value returned by model.say_hello
            message = self.model.say_hello(name)
            # render it by using example/hello.tpl template
            return template('example/hello', message=message)
        
        # Routing will be defined later
        # http://localhost:8080/hello
        # http://localhost:8080/hello?name=Haruna
        def hello_get(self):
            ##################################################################################
            # get URL query parameter                                                        #
            # (e.g: http://localhost:8080/hello?name=Haruna)                                 #
            # if you want to catch POST request, you can use request.POST                    #
            # I also give PHP equivalent code as comment:                                    #
            ##################################################################################
            # Python                            # PHP                                        #
            ##################################################################################
            name = None                         # $name = NULL;                              #
            if 'name' in request.GET:           # if(isset($_GET['name']))                   #
                name = request.GET['name']      #    $name = $_GET['name'];                  #
            ##################################################################################
            # get value returned by model.say_hello
            message = self.model.say_hello(name)
            # render it by using example/hello.tpl template
            return template('example/hello', message=message)
        
        # Routing will be defined later
        # http://localhost:8080/pokemon
        def pokemon(self):
            pokemons = self.model.get_pokemon()
            return template('example/pokemon', pokemons=pokemons)
    
    # make a Hello_Controller instance
    my_controller = Hello_Controller()
    
    # route to class method
    app.route("/hello", method='GET')(my_controller.hello_get)
    app.route("/hello/<name>")(my_controller.hello_param)
    app.route("/pokemon")(my_controller.pokemon)
```

Using procedural style, you can define your routing with __@app.route()__ decorator.
Using OOP style, you can use __app.route()__.

One thing I like from CodeIgnniter is automatic routing. Not many python framework provide such a thing.
Web2py also provide such a mechanism. In kokoropy, you are free to choose, wether to use manual routing or automatic one.
To use automatic routing feature, you should use __Default_Controller__ as your controller class name.
The automatic routing will produce such an url: __http://your_domain:your_port/your_application_directory/your_controller_file/published_function_name/parameter1/parameter2/etc
If your_application_directory and you_controller_file named "index", it can be omitted.
Your published function should have __action__ prefix (e.g: action_index will be published as index, action_hello will be published as hello)

In kokoropy you can even use those 3 different approach in just one file.

To know more about routing, please visit http://bottlepy.org/docs/dev/tutorial.html#request-routing .
To know more about request, please visit http://bottlepy.org/docs/dev/tutorial.html#request-data

View
----
It is wise to not put presentation logic in your controller. That's why we have view.

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

pokemon.tpl will be included in base.tpl and override %include.
As you see, you can also put some (limitted) python script in the template.
To know more about template, please visit http://bottlepy.org/docs/dev/stpl.html
