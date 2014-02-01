%rebase('index/views/base.tpl', title='kokoropy | getting started')
<style type="text/css">
    .language-python{
        width:100%;
        min-height: 200px;
    }
    .ace_editor{
        font-size: 14px;
    }
</style>
<script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/jquery-ace/ace/ace.js"></script>
<script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/jquery-ace/ace/theme-twilight.js"></script>
<script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/jquery-ace/ace/mode-python.js"></script>
<script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/jquery-ace/ace/mode-html.js"></script>
<script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/jquery-ace/jquery-ace.min.js"></script>
<script type="text/javascript">
    $(document).ready(function(){
        $('.language-python').ace({
            theme: 'twilight',
            lang: 'python',
        });
    });
</script>

<h2>Installation</h2>

<p>Kokoropy is a python web framework. 
Therefore you need to have python (recommended python 2.7) installed in your computer.
</p>

<p>Linux &amp; MacOS user does not need to worry anything since those OS have python pre-installed by default.
Windows user should download and install python. Personally, I suggest you to use <a href="https://www.enthought.com/products/canopy/">Enthought Canopy Distribution</a>
since it already has some libraries such as numpy &amp; matplotlib.<br />
If you are using debian-based linux (such as ubuntu) you can also (optionally) install numpy &amp; matplotlib by using following command:
<pre>
sudo apt-get install python-numpy
sudo apt-get install python-matplotlib
</pre>
If you are using python 3, you will need to install `python3-beaker` package
<pre>
sudo apt-get install python3-beaker
</pre>
</p>

<p>After All prerequisites met, you can just start kokoropy by using this command:
<pre>
cd path/to/kokoropy
python start.py
</pre>
</p>

<p>Now, open up your browser, and type <pre>http://localhost:8080</pre> in the address bar</p>

<h2>Kokoropy's Directory Structure</h2>
<p class="alert alert-info">This is just informational, you don't have to do anything</p>
<p>Just like every MVC framework, kokoropy has a typical directory structure. 
At the development stage, you only need to pay attention to <strong>/applications</strong> directory (this is where your applications laid)
and <strong>start.py</strong> file (this is where you put your configuration)
<pre>
    kokoropy
        |--- /applications                THIS IS WHERE YOUR APPLICATIONS LAID
        |       |--- __init__.py          * application's bootstrap
        |       |
        |       |--- /example             * example application
        |       |       |--- __init__.py  * application's __init__.py
        |       |       |--- /assets      * application's static files
        |       |       |--- /models      * application's models
        |       |       |--- /controllers * application's controllers
        |       |       |--- /views       * application's views
        |       |       |--- routes.py    * application's routes
        |       |
        |       |--- /index               * index application
        |       |       |--- __init__.py  * application's __init__.py
        |       |       |--- /assets      * application's static files
        |       |       |--- /models      * application's models
        |       |       |--- /controllers * application's controllers
        |       |       |--- /views       * application's views
        |       |       |--- routes.py    * application's routes
        |       |
        |       |--- /[your_application]  * your application
        |       |       |--- __init__.py  * application's __init__.py
        |       |       |--- /assets      * application's static files
        |       |       |--- /models      * application's models
        |       |       |--- /controllers * application's controllers
        |       |       |--- /views       * application's views
        |       |       |--- routes.py    * application's routes
        |
        |--- /kokoropy                    THIS IS WHERE KOKOROPY'S CORE LAID
        |       |--- __init__.py          * __init__.py
        |       |--- /beaker              * beaker package
        |       |--- /sqlalchemy          * sqlalchemy package
        |       |--- bottle.py            * bottle module
        |       |--- kokoro.py            * kokoropy's main program
        |
        |--- /db                          DATABASE EXAMPLE 
        |
        |--- README.md                    DOCUMENTATION & TUTORIAL
        |
        |                                 DEVELOPMENT & DEBUGGING 
        |--- start.py                     * script to run bootstrapper.py
        |--- bootstrapper.py              * bootstrapper
        |
        |                                 APACHE DEPLOYMENT FILES
        |--- kokoro.wsgi                  * bootstrapper for apache
        |--- kokoro.apache_conf           * configuration example
        |
        |                                 HEROKU DEPLOYMENT FILES
        |--- heroku.sh                    * heroku command example
        |--- heroku_app.py                * bootstrapper for heroku
        |--- Procfile                     * heroku specific file
        |--- runtime.txt                  * heroku specific file
        |--- requirements.txt             * heroku specific file
</pre>
In kokoropy, every application should contains <strong>__init__.py</strong> file.</p>
<p>The same rule is also applied to application's <b>models</b> and <b>controllers</b> directory.
You should also put an <b>__init__.py</b> inside each of them.
</p>

<h2>Configuration</h2>
<p>If you don't find anything wrong on the installation step, you can just ignore this part and go directly to installation.
Otherwise, if you find port 8080 already used another program (let's say django or web2py), you can change the port to 8081, 8082, or any different number.
To modify the configuration, open up start.py and look for these lines:
<pre>
HOST                = 'localhost'               # the server name
PORT                = 8080                      # http port
DEBUG               = True                      # True or False
RELOADER            = False                     # True or False
SERVER              = 'kokoro'                  # or wsgiref or whatever
APP_DIRECTORY       = 'applications'            # applications package
RUNTIME_PATH        = '.development_runtime'    # runtime path
BASE_URL            = '/kokoropy'               # base url, start with '/'
</pre>
</p>

<h2>Simplest Hello world</h2>
<p>Okay, let's try your first hello world program</p>
<p>first, make directory inside <b>/applications</b>, name it as <b>demo</b>. Create <b>__init__.py</b> and <b>routes.py</b>
<pre>
    kokoropy
        |--- /applications
        |       |--- __init__.py
        |       |
        |       |--- /demo                * (1. Make demo directory)
        |       |       |--- __init__.py  * (2. Make __init__.py)
        |       |       |--- routes.py    * (3. Make routes.py)
      (...)   (...)
</pre>
</p>
<p>Now, edit your routes.py and put this:
<textarea class="language-python" readonly="readonly">
from kokoropy import route, base_url

@route(base_url('hello))
@route('hello')
def say_something()
    return '<h1>Hello</h1><p>Nice to meet you</p>';
</textarea>
</p>
