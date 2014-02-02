Kokoropy
=========

A 心から Educational MVC Python Web Framework.

In japanese, kokoro means heart.
I make Kokoropy because I can not find any python web-framework which I really comfort with.
Some are too verbose, while some others have too many "magic". Most of them force me to learn about the framework, and do not allow me to directly focus on my job.
Basically I expect an easy-to-use framework like CodeIgniter (with more features) in python.

If you are in the same boat with me, then kokoropy is also for you.

Kokoropy is built in top of Bottle.py (http://bottlepy.org/docs/dev/), a very great python micro-web-framework.
While bottle.py focus on how to make things as simple as possible, kokoropy focus on how to make things as easy as possible.

Kokoropy is built based on my experiences with some framework. Here are some comparison between kokoropy and other framework

* Kokoropy is explicit & transparent. There is no magic in kokoropy. If you need something, you need to import it.
* You can use route directive just like in `bottle.py` (http://bottlepy.org), since bottle.py is the core of kokoropy.
* Kokoropy is built based on HMVC pattern. You can make unlimited number of separated MVC triad. This is good to make your application maintainable.
* Kokoropy doesn't have any other dependencies beside python-standard-library. You can even run it without Apache or nginx.
* Kokoropy support many database system. Every model can has its own database.
* Kokoropy support REST.
* Kokoropy support both, automatic and manual routing.
* Kokoropy support SESSION and COOKIES out of the box

__PS:__ This is my pet-project, and might be not stable. It is not ready for production purpose (yet)

Kokoropy stands in the shoulder of the giants. Here are projects that make kokoropy possible:
* bottlepy 0.12 dev (https://github.com/defnull/bottle)
* sqlalchemy 0.9.0 dev (https://github.com/zzzeek/sqlalchemy)
* beaker 1.6.4 (https://github.com/bbangert/beaker)

Also, kokoropy come with several third-party css & javascript framework (so you do not need to download them anymore):
* jquery 1.11.0
* jquery-ui 1.10.4
* jquery-mobile 1.4.0
* bootstrap 3.0.3
* colorbox 1.4.33
* chosen 1.0.0
* leaflet 0.7.2
* alertify.js 0.3.1.1
* jquery-ace 1.0.3

Documentation & Demo
====================
http://kokoropy.herokuapp.com

Who Kokoropy is for?
====================

Kokoropy is for you if you:

* Already familiar with PHP framework such as CodeIgniter but want to move to Python.
* Want to have a "educational" web framework that can be run everywhere.
* Desire explicity of framework, so that popular IDE such as eclipse can help in auto-completion (intellisense).
* Don't like complicated framework, you want a framework with small learning steep.


Deploy kokoropy on apache web server
================================================
This is how to deploy kokoropy on apache web server (assuming you use ubuntu or debian):
* You need to have mod-wsgi enabled.
* If you do not have mod-wsgi installed, please do: `sudo apt-get install libapache2-mod-wsgi`.
* If you do not have mod-wsgi enabled, please do: `sudo a2enmod wsgi`.
* Copy `kokoro.apache_conf`, put it on `/etc/apache2/sites-available/kokoro.apache_conf` (For other OS, please append this file contents to `httpd.conf`).
* Enable this configuration by doing: `sudo a2ensite kokoro.apache_conf`.
* Modify `/etc/apache2/sites-available/kokoro.apache_conf` as follows:
  - Replace every `/home/gofrendi/workspace/kokoropy` with your kokoropy directory location.
  - In case of you already have php installed, please don't use `localhost` as ServerName. Use another valid ServerName instead.
  - You can add valid ServerName by add a line at /etc/hosts (e.g: `127.0.1.1    arcaneSanctum` will add `arcaneSanctum` as valid ServerName).
  - Note, that by default apache will greedily take over every request and left nothing to be handled by your application. If you are using ubuntu/debian, modify `/etc/apache2/sites-enabled/000-default`. Change this part `<VirtualHost *:80>` into `<VirtualHost localhost:80>`
* Reload your apache by using `sudo service apache2 reload`. If it does not work, restart your apache by using `sudo service apache2 restart`

Deploy kokoropy on heroku
=====================================
This is how to deploy kokoropy on heroku (assuming you use ubuntu):
* Make heroku account, and visit https://devcenter.heroku.com/articles/python for more detail instruction
* get and install heroku toolbelt by using this command: `wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh`. For other OS, please visit the heroku website for more information.
* init a git repo by using this command: `git init`
* login to heroku (make sure you already have an account on heroku.com) by using this command: `heroku login`
* Set up heroku with a special buildpack (needed for matplotlib demo) by using this command `heroku create --buildpack https://github.com/dbrgn/heroku-buildpack-python-sklearn/`
* If you do not need matplotlib at all, just do `heroku create`
* If you have already do `heroku create` but change your mind later, and think that you need matplotlib, do this: `heroku config:set BUILDPACK_URL=https://github.com/dbrgn/heroku-buildpack-python-sklearn/`
* make heroku_app.py installable by using this command `chmod a+x heroku_app.py`
* detect all changes and deploy by using commit & push
```
    git add . -A
    git commit -m "Initial commit for heroku deployment"
    git push heroku master
```

Additional tips & tricks
====================================
* In Kokoropy, there is a `base_url` function that return absolute url relative to the BASE URL configuration

    ```python
        from kokoropy import route, base_url
        
        """
        Simple routing (without OOP)
        This is great to make a "hello world" or other small applications
        """
        @route(base_url('example/simple/hello_world'))
        def index():
            html_response  = 'This is just a very simple hello world !!!<br />'
            html_response += '<a href="'+base_url('/example/recommended')+'">See cooler things here</a>'
            return html_response
    ```
    
* Using Template function in kokoropy add special tag `{{ BASE_URL }}` and `{{ RUNTIME_PATH }}`, even if you dont define this

    ```python
        from kokoropy import route, base_url, template
        @route(base_url('/try'))
        def action_index(self, name=None):
            message='I love you'            
            return template('example/hello', message=message)
    ```
    ```html
        This is the message:  {{ message }}
        This is the BASE URL: {{ BASE_URL }}
        This is the RUNTIME PATH: {{ RUNTIME_PATH }}
        This is a link: <a href="{{ BASE_URL }}example/simple/hello_world">Click Me !!!</a>
    ```
    
* You can use `draw_matplotlib_figure` to draw something by using matplotlib

    ```python
        from kokoropy import base_url, draw_matplotlib_figure
        @route(base_url('plot'))
        def action_plot(self):
            # import things
            import numpy as np
            from matplotlib.figure import Figure
            # x = {1, 2, 3, ..., 10}; y = x*x
            x = np.arange(0, 10, 1)
            y = np.square(x)
            # make figure       
            fig = Figure()
            fig.subplots_adjust(hspace = 0.5, wspace = 0.5)
            # first subplot
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(x, y1, 'b')
            ax.plot(x, y1, 'ro')
            ax.set_title ('y = x^2')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            # make canvas
            return draw_matplotlib_figure(fig)
    ``` 

* You can accessing session by using `request['SESSION']` which is basically the same as `request.environ['beaker.session']`
* You can and encouraged to use automatic routing as described in tutorial 2.

Change Log:
===========
* Provide `base_url` setting (done, tested, 2013/08/08)
* In debugging session (via `python start.py`), auto reload server when something changed (done, tested, 2013/08/08)
* Add request.BASE_URL to every view & link in the example (done, tested, 2013/08/09)

TODO:
====
* Make CRUD generator
