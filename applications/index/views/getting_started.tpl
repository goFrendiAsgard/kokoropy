%rebase('index/views/base.tpl', title='kokoropy | getting started')
<style type="text/css">
    .language-python, .language-html{
        width:100%;
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
        $('.language-html').ace({
            theme: 'twilight',
            lang: 'html',
        });
    });
</script>

<h1>Setting</h1>
<h2>Installation</h2>

<p>
    Kokoropy is a python web framework. 
    Therefore you need to have python (recommended python 2.7) installed in your computer.
</p>

<p>
    Linux &amp; MacOS user does not need to worry anything since those OS have python pre-installed by default.
    Windows user should download and install python. Personally, I suggest you to use <a href="https://www.enthought.com/products/canopy/">Enthought Canopy Distribution</a>
    since it already has some libraries such as numpy &amp; matplotlib.<br />
    If you are using debian-based linux (such as ubuntu) you can also (optionally) install numpy &amp; matplotlib by using following command:
</p>
<pre>
sudo apt-get install python-numpy
sudo apt-get install python-matplotlib
</pre>
<p>
    If you are using python 3, you will need to install `python3-beaker` package
</p>
<pre>
sudo apt-get install python3-beaker
</pre>

<p>
    After All prerequisites met, you can just start kokoropy by using this command:
</p>
<pre>
cd path/to/kokoropy
python start.py
</pre>

<p>
    Now, open up your browser, and type
</p>
<pre>http://localhost:8080</pre> 
<p>
    in the address bar
</p>

<h2>Kokoropy's Directory Structure</h2>
<p class="alert alert-info"><b>Don't worry</b> This is just informational, you don't have to do anything</p>
<p>
    Just like every MVC framework, kokoropy has a typical directory structure. 
    At the development stage, you only need to pay attention to <strong>/applications</strong> directory (this is where your applications laid)
    and <strong>start.py</strong> file (this is where you put your configuration)
</p>
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
<p>
    In kokoropy, every application should contains <strong>__init__.py</strong> file.
</p>
<p>
    The same rule is also applied to application's <b>models</b> and <b>controllers</b> directory.
    You should also put an <b>__init__.py</b> inside each of them.
</p>

<h2>Configuration</h2>
<p class="alert alert-info"><b>Don't worry</b> You will only need to fiddle up with configuration if port 8080 is already used by other application. Otherwise, you can skip this part safely</p>
<p>
    If you don't find anything wrong on the installation step, you can just ignore this part and go directly to installation.
    Otherwise, if you find port 8080 already used another program (let's say django or web2py), you can change the port to 8081, 8082, or any different number.
    To modify the configuration, open up start.py and look for these lines:
</p>
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

<h1>Coding</h1>

<h2>Simplest Hello world</h2>
<p>Okay, let's try your first hello world program</p>
<p>first, make directory inside <b>/applications</b>, name it as <b>demo</b>. Create <b>__init__.py</b> and <b>routes.py</b>
</p>
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
<p>
    Now, edit your routes.py and put this:
</p>
<textarea class="language-python" readonly="readonly" style="height:150px;">
from kokoropy import route, base_url

@route(base_url('hello))
@route('hello')
def say_something():
    return '<h1>Hello</h1><p>Nice to meet you</p>';
</textarea>
<p>
    The first line used to tell python interpreter that we will need <b>route</b> decorator and <b>base_url</b> function.<br />
    The third and fourth line tell kokoropy so that both <b>http://localhost:8080/kokoropy/hello</b> and <b>http://localhost:8080/kokoropy/hello</b> will be handled by <b>say_something</b> function<br />
    The function will return a html response as described.<br />
    To get more comprehensive documentation about <b>route</b> decorator, please visit <a href="http://bottlepy.org/docs/dev/tutorial.html#request-routing">Bottle's documentation about request routing</a>
</p>

<h2>MVC and automatic routing</h2>
<p>
    You might need something more complex than just a typical "hello world" program.<br />
    It's not good to put everything in <b>routes.py</b>, since it will be to complicated to be maintained.<br />
    Here is where MVC rocks. MVC stands for <b>M</b>odel, <b>V</b>iew, <b>C</b>ontroller.<br />
</p>
<ul>
    <li><b>Model</b> is the heart of your application. It define what an application can do. Imagine it as a bunch of functions which are ready to be used anytime.
    Model is usually, but not neccesaryly associated to database. People tend to write their database scripts (either using ORM or raw SQL) in model.
    </li>
    <li><b>Controller</b> is a gateway of your application. It define how user can interact with your application. A request from client wil be delivered to your controller.
    The controller then do some action, and call some routines defined in the model. And as visual feedback, controller will load a view and return it as response.
    </li>
    <li><b>View (or Template)</b> is a visual matter. You should put your HTML, javascript, and css here.</li>
</ul>
<p>
    Let's make your first MVC in kokoropy
</p>
<pre>
    kokoropy
        |--- /applications
        |       |--- __init__.py
        |       |
        |       |--- /demo                              * ( 1. Make demo directory)
        |       |       |--- __init__.py                * ( 2. Make __init__.py)
        |       |       |--- routes.py                  * ( 3. Make routes.py)
        |       |       |--- /models                    * ( 4. Make models directory)
        |       |       |       |--- __init__.py        * ( 5. Make __init__.py)
        |       |       |       |--- my_model.py        * ( 6. Make my_model.py)
        |       |       |--- /controllers               * ( 7. Make controllers directory)
        |       |       |       |--- __init__.py        * ( 8. Make __init__.py)
        |       |       |       |--- my_controller.py   * ( 9. Make my_controller.py)
        |       |       |--- /views                     * (10. Make views directory)
        |       |       |       |--- my_view.tpl        * (11. Make my_view.py)
      (...)   (...)
</pre>
<h3>Model</h3>
<p>
    Put this in <b>my_model.py</b> (Don't worry about the script, I'm using sqlalchemy ORM, but you can use standard SQL if you think it is going to be better):
</p>
<textarea class="language-python" readonly="readonly" style="height:800px;">
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

############################### SQL ALCHEMY SCRIPT ####################################

# create Base
Base = declarative_base()

# create Pokemon class
class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    
    def __init__(self, name, image):
        self.name = name
        self.image = image

# create engine
engine = create_engine('sqlite:///db/pokemon.db', echo=True)

# create db session
db_session = scoped_session(sessionmaker(bind=engine))

#################################### OUR MODEL #######################################

class My_Model(object):
    '''
    Create, Update & Delete Pokemon data
    '''
    def __init__(self):
        Base.metadata.create_all(bind=engine)
    
    def get_pokemon(self, keyword=''):
        return db_session.query(Pokemon).filter(Pokemon.name.like('%'+keyword+'%')).all()
</textarea>

<h3>Controller</h3>
<p>
    Put this in <b>my_controller.py</b>:
</p>
<textarea class="language-python" readonly="readonly" style="height:270px;">
from kokoropy import Autoroute_Controller, load_view, load_model
class My_Controller(Autoroute_Controller):
    
    def __init__(self):
        # import models
        My_Model = load_model('demo', 'my_model')
        self.model = My_Model()
        
    def action_pokemon(self, keyword=None):
        # get pokemons
        pokemon_list = self.model.get_pokemon(keyword)
        return load_view('demo', 'my_view', pokemon_list = pokemon_list)
</textarea>

<h3>View</h3>
<p>
    Put this in <b>my_view.py</b>:
</p>
<textarea class="language-html" readonly="readonly" style="height:500px;">
<h3>Pokemon List</h3>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>Pokemon Name</th>
            <th>Image</th>
        </tr>        
    </thead>
    <tbody>
        &#37;for pokemon in pokemons:
        <tr>
            <td>&#123;&#123; pokemon.name &#125;&#125;</td>
            <td>
                &#37;if pokemon.image == '':
                <img src="&#123;&#123; BASE_URL &#125;&#125;demo/assets/images/pokemon-no-image.png" style="height:65px;" />
                &#37;else:
                <img src="&#123;&#123; BASE_URL &#125;&#125;demo/assets/uploads/&#123;&#123; pokemon.image &#125;&#125;" style="height:65px;" />
                &#37;end
            </td>
        </tr>
        &#37;end        
    </tbody>      
</table>
</textarea>
