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
