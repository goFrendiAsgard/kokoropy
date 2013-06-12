Kokoropy
=========

A MVC python web framework, from my heart <3

In japanese, kokoro means heart.
I make Kokoropy because I can not find any python web-framework which I really comfort with.
Some are too verbose, while some others have too many "magic". Most of them force me to learn about the framework, and not allow me to focus on my job.
Basically I expect an easy framework like CodeIgniter (of course, with more features) in python.

If you are in the same boat with me, then kokoropy is for you.

Kokoropy is built in top of Bottle.py (http://bottlepy.org/docs/dev/), a very great python micro-framework.
While bottle.py focus on how to make things as simple as possible, kokoropy focus on how to make things as easy as possible.
If you've once ever use my another open source project, No-CMS (http://getnocms.com), you will know what I mean by easy.

Kokoropy is built based on my experiences with some framework. Here are some comparison between kokoropy and other framework

* Kokoropy is explicit. There is no such a "magic" like in web2py.
* You can use route directive in bottle.py, since bottle.py is the core of kokoropy.
* Kokoropy is built based on HMVC pattern, like laravel, fuelPHP and CodeIgniter+HMVC.
* Kokoropy doesn't have any other dependencies. You can even run it without Apache or nginx, just like web2py.
* Kokoropy support many database system. Every model can has its own database.
* Kokoropy support REST.
* Kokoropy support both, automatic and manual routing.
* Kokoropy support SESSION out of the box

__PS:__ This is my pet-project, and might be not stable. It is not ready for production purpose (yet)

Kokoropy come with bottlepy 0.12 dev, sqlalchemy 0.7.11, and beaker 1.6.4 included

Who Kokoropy is for?
====================

Kokoropy is for you if you:

* Already familiar with PHP framework such as CodeIgniter but want to move to Python.
* Want to have a "educational" web framework that can be run everywhere.
* Desire explicity of framework, so that popular IDE such as eclipse can help in auto-completion (intellisense).
* Don't like complicated framework, you want a framework with small learning steep.


Configuration & Getting Started
===============================

Configuring Kokoropy is very easy. Just open up start.py, and do some modification.
For development purpose, it is recommended to leave the configuration as it is.

```python
    HOST                = 'localhost'
    PORT                = 8080
    DEBUG               = True
    RELOADER            = False
    SERVER              = 'wsgiref'
    APP_DIRECTORY       = 'applications'
```
APP_DIRECTORY contains of your applications directory.
Other configuration are just like bottlepy configuration.

You can start the server by using this command:
```
    python start.py
```

Once the server started up, you can access your web application by using any browser.
```
    http://localhost:8080
```

Overview
========

Kokoropy use HMVC architecture. HMVC stands for Hiearchical Model-View-Controller.
In Kokoropy, your web contains several ```application```.
Each application consists of several ```model```, ```view```, and ```controller```

* Models are hearts of your application. It define what an application can do.
* Controllers are gateways of your application. Models make your application able to do things, but controller make your application do things
* Views are presentations of your application. It deals with user interfaces

Directory Structure
===================

Below is Kokoropy directory structure.

```
    kokoropy
        |--- applications                (contains your applications)
        |       |--- __init__.py         (application's bootstrap)
        |       |--- [an_application]    (an application)
        |               |--- assets      (application's static files)
        |               |--- models      (application's models)
        |               |--- controllers (application's controllers)
        |               |--- views       (application's views)
        |               |--- __init__.py (application's bootstrap)
        |
        |--- kokoropy                    (the core of kokoropy, you
        |       |                         probably don't need to be here)
        |       |--- __init__.py         (Kokoropy's core script)
        |       |--- beaker              (beaker package)
        |       |--- sqlalchemy          (sqlalchemy package)
        |       |--- bottle.py           (bottle module)
        |
        |--- start.py                    (application starter script)
        |--- db                          (sample database used for
        |                                 example application)
        |--- .runtime                    (runtime directory, contains
                                          copy of all assets, view, and session)
```

__Note :__ applications, models and controllers are python packages. It shall contains at least ```___init__.py``` file.
To understand about package in python, please visit http://docs.python.org/2/tutorial/modules.html#packages


Tutorial 1: Hello World
=======================
In Kokoropy make a "hello world" is very simple.
You only need to make an application that consists of a controller.

```
    applications
        |--- index
        |--- example
        |--- your_app                    (1. Create this directory)
                |--- __init__.py         (2. Create empty __init__.py file
                |                            to turn your_app into python package)
                |--- controllers         (3. Create this directory)
                        |--- __init__.py (4. Create empty __init__.py file
                        |                    to turn controllers into python package)
                        |--- hello.py    (5. This is your controller)
```

On `applications/your_app/controllers/hello.py`, write this:

```python
    from kokoropy import route

    @route('/hello_world')
    def index(self):
        # return response
        return '''
            <title>Kokoropy</title>
            <h1>Hello world</h1>'''
```

Run kokoropy server (if it is already started, then restart it by pressing ctrl+c, and run it again)
```
    python start.py
```

Open your browser, and access
```
    http://localhost:8080/hello_world
```

Below is explanation of the code:

* ```from kokoropy import route``` : import route from Kokoropy's core. By having route, you can use ```@route``` decorator
* ```@route('/hello_world')``` : so, from now on if user open http://localhost:8080/hello_world, Kokoropy will return a response returned by ```index``` function
* if you want to return a single line response, you can use double quote ```"``` or single quote ```'```
* if you want to return a multi line response, you can use triple double quote ```"""``` or triple single quote ```'''```

__Note:__ Doing a manual routing like this can lead to confusion if you work on a team and everyone define their own route.
To know more about routing, please visit http://bottlepy.org/docs/dev/tutorial.html#request-routing


Tutorial 2: Automatic Routing
=============================

In most cases, your application might contains more than just hello world. Therefore defining routing manually will be tiresome.
Kokoropy support automatic routing. Using automatic routing is very easy:

* In controller there should be a class named ```Default_Controller```
* Any published function should has ```action_``` prefix
* Beside ```action_``` prefix, you can also use REST prefixes:
    - ```act_get_``` : only accept get request
    - ```act_post_``` : only accept post request
    - ```act_delete_``` : only accept delete request
    - ```act_put_``` : only accept put request
* Every automatic routed
* Automatic routing works this way: ```http://domain:port/application/controller_filename/action_function_without_prefix/parameter_1/parameter_2
* If ```application```, ```controller_filename``` or, ```action_function_without_prefix``` is equal to "index", it can be omitted

Now modify ```hello.py``` into this:

```python
    class Default_Controller(object):

        def action_index(self):
            # return response
            return '''
                <title>Kokoropy</title>
                <h1>Hello world</h1>'''

        def action_welcome(self, name = None):
            if name is None:
                name = 'Stranger'
            response = '<title>Kokoropy</title><h1>Welcome '+name+'</h1>'
            return response
```

Run kokoropy server (if it is already started, then restart it by pressing ctrl+c, and run it again)
```
    python start.py
```

Open your browser, and access these addresses:
```
    http://localhost:8080/your_app/hello/
    http://localhost:8080/your_app/hello/index
    http://localhost:8080/your_app/hello/welcome
    http://localhost:8080/your_app/hello/welcome/John
    http://localhost:8080/your_app/hello/welcome/John%20Titor
    http://localhost:8080/your_app/hello/welcome/Ryuzaki
```

Explanation:
* Name of your application is ```your_app```. It is located at ```applications/your_app```
* Your controller file_name is ```hello```. It is located at ```application/your_app/controllers/hello.py```
* In ```hello.py``` you have a class named ```Default_Controller```. This make Kokoropy's automatic routing works
* Since automatic routing works, you don't need to import route from Kokoropy. So, in this tutorial, you don't see any ```from kokoropy import route```
* In Default_Controller, you have 2 functions with ```action_``` prefix. ```action_index``` and ```action_welcome``` are published as ```index``` and ```welcome``` respectively.
* ```action_welcome``` has ```name``` parameter. The parameter has default value ```None```. So when you access ```http://localhost:8080/your_app/hello/welcome/John``` the name parameter will be ```"John"```,
  but when you access ```http://localhost:8080/your_app/hello/welcome```, the name will be ```None``` as its default value.

__Note:__ When you work with team, automatic routing is recommended. It make things simple and easy to be tracked

Tutorial 3: Handling request
============================
To handle request you will need request object.
You can use:
* ```request.GET``` to catch get request as using $_GET in PHP
* ```request.POST``` to catch post request as using $_GET in PHP
* ```request.SESSION``` to get session as using $_SESSION in PHP (request.session is actually wrapper for ```request.environ["beaker.session"]```)
* ```request.file``` to handle file upload

Modify ```hello.py``` into this:

```python
    import os
    from kokoropy import request

    class Default_Controller(object):

        def action_index(self):
            # return response
            return '''
                <title>Kokoropy</title>
                <h1>Hello world</h1>'''

        def action_welcome(self, name = None):
            if name is None:
                name = 'Stranger'
            # get name from get request
            if 'name' in request.GET:
                name = request.GET['name']
            # build response and return it
            response = '<title>Kokoropy</title><h1>Welcome '+name+'</h1>'
            return response

        def action_upload(self):
            upload =  request.files.get('uploaded_file')
            upload_path = os.path.dirname(os.path.dirname(__file__))+'/assets/'
            upload.save(upload_path)
            return 'Upload success'
```

Make a html file or another function that return a html code of form upload:
```html
    <form action="http://localhost:8080/your_app/hello/upload" method="post" enctype="multipart/form-data">
      Select a file: <input type="file" name="uploaded_file" />
      <input type="submit" value="Start upload" />
    </form>
```

__Note:__ To know more about request, please visit http://bottlepy.org/docs/dev/tutorial.html#request-data

Tutorial 4: Model & Database
============================
So far, we have play around with Controller. Basically, without Model & View, you can make a working web application.
But please, do not stop here. Put everything in your controller is a bad practice, and will lead into complicated spaghetti code.
You need to separate your application into Model-View-Controller.

Let's make another controller in your_app
```
    applications
        |--- index
        |--- example
        |--- your_app
                |--- __init__.py
                |--- controllers
                |       |--- __init__.py
                |       |--- hello.py
                |       |--- pokemon.py        (1. Create a new controller)
                |
                |--- models                    (2. Create a models directory)
                        |--- __init__.py       (3. Create empty __init__.py file
                        |                          to make models a package)
                        |--- pokemon_model.py  (4. Create a model)
```

Now, take a look on pokemon.py.

Basically you can make something like this:
```python

    class Default_Controller(object):

        def action_index():
            # return response
            return '''
                <title>Pokemon</title>
                <ul>
                    <li>Pikachu</li>
                    <li>Bulbasur</li>
                    <li>Squirtle</li>
                    <li>Charmender</li>
                    <li>Caterpie</li>
                </ul>'''
```

Or you can make it a bit better:
```python

    class Default_Controller(object):

        def action_index(self):
            # define pokemon list
            pokemon_list = ['Pikachu', 'Bulbasur', 'Squirtle', 'Charmender', 'Caterpie']
            # define ul
            ul = '<ul>';
            for pokemon in pokemon_list:
                ul += '<li>'+pokemon+'</li>'
            ul += '</ul>'
            # return response
            return '<title>Pokemon</title>' + ul
```

Or even better:
```python

    class Default_Controller(object):

        def action_index(self):
            # define pokemon list
            pokemon_list = ['Pikachu', 'Bulbasur', 'Squirtle', 'Charmender', 'Caterpie']
            # return response
            return '<title>Pokemon</title>' + self.build_ul(pokemon_list)

        def build_ul(self, list):
            ul = '<ul>';
            for item in list:
                ul += '<li>'+item+'</li>'
            ul += '</ul>'
```

Now, suppose you have an sqlite database contains a pokemon table located at ```db/pokemon.db```. (Actually it is really there)
And you want to take the pokemon list from the database. You can do something like this:

```python
    import sqlite3

    class Default_Controller(object):

        def action_index(self):
            # define pokemon list
            conn = sqlite3.connect("db/pokemon.db")
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM pokemon_list")
            pokemon_data = self.cursor.fetchall()
            print(pokemon_data) # in case of you are curious how the pokemon_data fetched
            pokemon_list = [x[0] for x in pokemon_list]
            # return response
            return '<title>Pokemon</title>' + self.build_ul

        def build_ul(self, list):
            ul = '<ul>';
            for item in list:
                ul += '<li>'+item+'</li>'
            ul += '</ul>'
```
Python come with a very handy sqlite driver. And any other database driver should refer to this standard.
the pokemon_data will consist of list of tupple. Every tupple consists of a row. So it gonna be something like this:
`[('pikachu'), ('charmender'), ('squirtle'), ('bulbasur')]`

Adding database capability make your controller become less-readable. And it's time to use Model.
Now, modify your `pokemon_model.py` into this:

```python
import sqlite3

class Pokemon_Model(object):

    def __init__(self):
        # define conn
        self.conn = sqlite3.connect("db/pokemon.db") # or use :memory: to put it in RAM
        self.cursor = self.conn.cursor()

    def fetch_pokemon(self, keyword=""):
        self.cursor.execute("SELECT name FROM pokemon_list WHERE name LIKE '%"+keyword+"%'")
        pokemon_data = self.cursor.fetchall()
        pokemon_list = [x[0] for x in pokemon_list]
        return pokemon_list
```

And your `pokemon.py` controller into this:

```python
    import applications.your_app.models.Pokemon_Model

    class Default_Controller(object):

        def action_index(self):
            pokemon_model = Pokemon_Model()
            pokemon_list = pokemon_model.fetch_pokemon()
            # return response
            return '<title>Pokemon</title>' + self.build_ul

        def build_ul(self, list):
            ul = '<ul>';
            for item in list:
                ul += '<li>'+item+'</li>'
            ul += '</ul>'
```

If it is just to fetch pokemon, you will probably not see many difference. But when it come to big application, you will see how useful is this approach.
Using model also let you keep yourself DRY (Dont Repeat Yourself)

Suppose you have a lot of controllers and most of them should fetch the pokemon. An amateur will ends up copy-pasting the pokemon-fetching code to every controller.
This way, modification going to be hard. Using model will save your life :)

Tutorial 5: View
================
You have see how useful a model is. Now let's take a look at view.
View is your presentation layer. In previous tutorial, we always mix up HTML into Controller. Imagine you have a lot of banner, javascript, css, etc, and your controller will be a spaghetti.
That is why you need a view.

Now, add a view folder:

```
    applications
        |--- index
        |--- example
        |--- your_app
                |--- __init__.py
                |--- controllers
                |       |--- __init__.py
                |       |--- hello.py
                |       |--- pokemon.py
                |
                |--- models
                |       |--- __init__.py
                |       |--- pokemon_model.py
                |
                |--- views                      (1. Create a view directory)
                        |--- pokemon.tpl        (2. Here is our view)
                        |--- base.tpl           (3. We will use it later)
```

Now, modify your `pokemon.py` controller into this:

```python
    from kokoropy import template
    import applications.your_app.models.Pokemon_Model

    class Default_Controller(object):

        def action_index(self):
            pokemon_model = Pokemon_Model()
            pokemon_list = pokemon_model.fetch_pokemon()
            return template('your_app/pokemon.tpl', list=pokemon_list)
```

And modify your `pokemon.tpl` into this:
```html
    <strong>Pokemon list:</strong>
    <ul>
    %for pokemon in list:
        <li>{{pokemon}}</li>
    %end
    </ul>
````

Explanation:
* `return template('your_app/pokemon.tpl', list=pokemon_list)` make `pokemon_list` is passed into `pokemon.tpl` as `list`
* In your view, you can do some limited python code by using `%` preceeding the code. But, unlike the usual way, you also need to explicitly put `%end` on every block.

Pretty neat isn't it?

View is not only help you separate presentation from the controller, but also help you to make keep yourself DRY.
For example, if you have a lot of pages, you will ends up writing banner, menu, and other trivial things in every pages.
That is why we need `rebase`.

Now modify your `pokemon.tpl` into this:

```html
    <strong>Pokemon list:</strong>
    <ul>
    %for pokemon in list:
        <li>{{pokemon}}</li>
    %end
    </ul>
    %rebase your_app/base
````

And modify your `base.tpl` into this:

```html
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="">
            <meta name="author" content="">
            <link rel="stylesheet" type="text/css" href="/assets/static_libraries/bootstrap/css/bootstrap.min.css" />
            <link rel="stylesheet" type="text/css" href="/assets/example/css/style.css" />
            <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
            <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
            <![endif]-->
            <script type="text/javascript" src="/assets/static_libraries/jquery.tools.min.js"></script>
            <script type="text/javascript" src="/assets/static_libraries/bootstrap/js/bootstrap.min.js"></script>
            <script type="text/javascript" src="/assets/example/js/script.js"></script>
            <title>Kokoropy</title>
        </head>
        <body>
            <div class="navbar navbar-inverse navbar-fixed-top">
                <div class="navbar-inner">
                    <div class="container">
                        <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                            <span class="icon-bar">&nbsp;</span>
                            <span class="icon-bar">&nbsp;</span>
                            <span class="icon-bar">&nbsp;</span>
                        </button>
                        <a class="brand" href="#">Kokoropy</a>
                        <div class="nav-collapse collapse">
                            <ul class="nav">
                                <li><a href="/example/simple/hello_world">Simple route</a></li>
                                <li><a href="/example/recommended/index">Recommended route</a></li>
                                <li><a href="/example/advance/hello">Advance route</a> </li>
                                <li><a href="/example/recommended/upload">Test upload file</a> </li>
                            </ul>
                        </div><!--/.nav-collapse -->
                    </div>
                </div>
            </div>

            <div id="content-container" class="container">
                <div class="row-fluid">
                    <div id="layout-banner" class="well hidden-phone span12">
                        <div class="span2">
                            <img src ="/assets/images/kokoropy.png" />
                        </div>
                        <div class="span10">
                            <h1>Kokoropy</h1>
                            <p>心から Python MVC Web Framework</p>
                        </div>
                    </div>
                    <div id="layout-content" class="span12">
                        <p id="content">%include</p>
                    </div><!--/#layout-content-->
                </div><!--/row-->
                <hr>
                <footer>GoFrendiAsgard &copy; 2013</footer>
            </div><!--/.fluid-container-->

        </body>
    </html>
```

Now, `pokemon.tpl` will also include `base.tpl`. The original content of `pokemon.tpl` will replace `%include` in `base.tpl`

__Note:__ To know more about template, please visit http://bottlepy.org/docs/dev/stpl.html

Tutorial 6: Deploy kokoropy on apache web server
================================================
This is how to use kokoropy with apache web server (assuming you use ubuntu or debian):
* You need to have mod-wsgi enabled.
* If you do not have mod-wsgi installed, please do: `sudo apt-get install libapache2-mod-wsgi`.
* If you do not have mod-wsgi enabled, please do: `sudo a2enmod wsgi`.
* Copy `kokoro.apache_conf`, put it on `/etc/apache2/sites-available/kokoro.apache_conf` (On another OS, please append this file contents to `httpd.conf`).
* Enable this configuration by doing: `sudo a2ensite kokoro.apache_conf`.
* Modify `/etc/apache2/sites-available/kokoro.apache_conf` as follows:
  - Replace every `/home/gofrendi/workspace/kokoropy` with your kokoropy directory location.
  - In case of you already have php installed, please don't use `localhost` as ServerName. Use another valid ServerName instead.
  - You can add valid ServerName by add a line at /etc/hosts (e.g: `127.0.1.1    arcaneSanctum` will add `arcaneSanctum` as valid ServerName).

TODO:
====
* Provide `base_url` setting (pending: for now, assume `/` as `base_url`)
* In debugging session (via `python start.py`), auto reload server when something changed (done)