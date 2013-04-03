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

__PS:__ This is my pet-project, and might be not stable. It is not ready for production purpose (yet)

Kokoropy come with bottlepy 0.12 dev, sqlalchemy 0.7.11, and beaker 1.6.4 included

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

kokoropy come with a basic example model located at /application/index/models/example_model.py

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

kokoropy come with a basic example controller located at /application/index/controllers/index.py

```python
    from kokoropy.bottle import template, request, route

    ## APPROACH 1 (Simple but deadly works) ##################################################
    #
    # A very simple procedural style example
    # Manually routed to http://localhost:8080/ with @route decorator
    ##########################################################################################

    @route('/hello_world')
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
            return template('example/hello', message='Automatic route working !!!', first_time=True)

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
    hello_controller = Hello_Controller()
    route("/hello", method='GET')(hello_controller.hello_get)
    route("/hello/<name>")(hello_controller.hello_param)
    route("/pokemon")(hello_controller.pokemon)
```

Using procedural style, you can define your routing with __@route()__ decorator.
Using OOP style, you can use __route()__.

One thing I like from CodeIgnniter is automatic routing. Not many python framework provide such a thing.
Web2py also provide such a mechanism. In kokoropy, you are free to choose, wether to use manual routing or automatic one.
To use automatic routing feature, you should use __Default_Controller__ as your controller class name.
Also Your published function should have __action__ prefix, just as FuelPHP way (e.g: action_index will be published as index, action_hello will be published as hello)

The automatic routing will produce such an url: http://your_domain:your_port/your_application_directory/your_controller_file/published_function_name/parameter1/parameter2

If your_application_directory and you_controller_file named "index", it can be omitted.


In kokoropy you can even use those 3 different approach in just one file.

To know more about routing, please visit http://bottlepy.org/docs/dev/tutorial.html#request-routing .
To know more about request, please visit http://bottlepy.org/docs/dev/tutorial.html#request-data

View
----
It is wise to not put presentation logic in your controller. That's why we have view.

You can separate your view into several template.
Let's say you have a baste template at /application/index/views/example/base.tpl

```html
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/index/css/style.css" />
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

and another template at /application/index/views/example/pokemon.tpl

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
