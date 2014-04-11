#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Repo: https://github.com/goFrendiAsgard/kokoropy
'''
__author__  = 'Go Frendi Gunawan'
__version__ = 'development'
__license__ = 'MIT'

###################################################################################################
# Add package directory to sys.path
###################################################################################################
import os, inspect, sys, shutil
from datetime import datetime
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(__file__),'packages'))

###################################################################################################
# Import things
###################################################################################################
import bottle, beaker, threading, time, tempfile, re, beaker.middleware
from bottle import default_app, debug, run, static_file,\
    response, request, TEMPLATE_PATH, route, get,\
    post, put, delete, error, hook, Bottle, redirect

from bottle import template as _bottle_template

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import desc

from colorama import init, Fore, Back
init()
############################### SQL ALCHEMY SCRIPT ####################################

# create Base
Base = declarative_base()

# create Migration class
class Migration(Base):
    __tablename__ = 'migration'
    id = Column(Integer, primary_key=True)
    signature = Column(String)
    migration_name = Column(String)
    
    def __init__(self, signature, migration_name):
        self.signature = signature
        self.migration_name = migration_name

###################################################################################################
# Hacks & Dirty Tricks :)
###################################################################################################  
# Python 3 hack for xrange
if sys.version_info >= (3,0,0):
    xrange = range
    from urllib.parse import urlparse
    from urllib.request import urlopen
else:
    from urlparse import urlparse
    from urllib2 import urlopen

# intellisense hack
request.SESSION = []

###################################################################################################
# KokoroWSGIRefServer (Do something with this in the future)
###################################################################################################
class KokoroWSGIRefServer(bottle.ServerAdapter):
    '''
    Original: http://stackoverflow.com/questions/11282218/bottle-web-framework-how-to-stop
    '''
    srv = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(self, *args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.srv = make_server(self.host, self.port, handler, **self.options)
        self.srv.serve_forever()

    def stop(self):
        if self.srv is not None:
            self.srv.shutdown()
            self.srv.server_close()

###################################################################################################
# Autoroute_Controller, actually doesn't do anything
###################################################################################################
class Autoroute_Controller(object):
    pass

# load view
def load_view(application_name, view_name, *args, **kwargs):
    args_list = list(args)
    args_list.insert(0, os.path.join(application_name , "views" , view_name))
    # get view_path (relative to template path
    if not request.BASE_URL is None:
        kwargs['BASE_URL'] = request.BASE_URL
    else:
        kwargs['BASE_URL'] = base_url()
    kwargs['RUNTIME_PATH']      = runtime_path()
    kwargs['app_path']  = application_path()
    # adjust args[0], add "'views' if it is not exits
    path_list = list(args_list[0].split('/'))
    if len(path_list) >= 2 and path_list[1] != 'views':
        path_list = [path_list[0],] + ['views',] + path_list[1:]
    # get view_path
    view_path = os.path.join(*path_list)    
    # get template's content
    default_extensions = ['html', 'tpl', 'stpl', 'thtml']
    extension = view_path.split('.')[-1]
    for template_path in TEMPLATE_PATH:
        if extension in default_extensions:
            path = os.path.join(template_path, view_path)
            if os.path.exists(path):
                break
        else:
            for default_extension in default_extensions:
                path = os.path.join(template_path, view_path + '.' + default_extension)
                if os.path.exists(path):
                    break
    content = file_get_contents(path)
    # add \n to prevent content rendeFore.RED as path
    if not '\n' in content:
        content = content + '\n'
    # create block pattern
    block_pattern = r'{%( *)block( *)([A-Za-z0-9_-]*)( *)%}((.|\n)*?){%( *)endblock( *)%}+?'
    # get block_chunks
    block_chunks = re.findall(block_pattern, content)
    # remove all literal block from content
    content = re.sub(block_pattern, r'', content)
    # get content by rendering template
    args_list[0] = content
    args = tuple(args_list)
    content = _bottle_template(*args, **kwargs)
    for chunk in block_chunks:
        block_name = chunk[2]
        block_content = chunk[4]
        # change {% parent %} into % __base_block_BLOCKNAME()\n
        block_content = re.sub(r'{%( *)parent( *)%}+?',
                               r'\n% __base_block_'+block_name+'()\n',
                               block_content)
        content = '% def __block_' + block_name + '():\n' + block_content + '\n% end\n' + content
    # change 
    #    {% block X %}Y{% endblock %}" 
    # into 
    #     % def __base_block_X:
    #         Y
    #     % end
    #     % setdefault('__block_X', __base_block_X)
    #     % __block_X()
    content = re.sub(block_pattern, 
                     r'% def __base_block_\3():\n\5\n% end\n% setdefault("__block_\3", __base_block_\3)\n%__block_\3()\n',
                     content)
    # render again
    args_list[0] = content
    args = tuple(args_list)
    content = _bottle_template(*args, **kwargs)
    return _bottle_template(*args, **kwargs)

# This class serve kokoropy static files routing & some injection into request object
class _Kokoro_Router(object):
    def before_request(self):
        """ Before request event
            Inject request.SESSION as alias of request.environ["beaker.session"]
            There is no need to call this function manually
        """
        request.SESSION = request.environ["beaker.session"]
        request.RUNTIME_PATH = runtime_path()
        request.APPLICATION_PATH = application_path()
        url = bottle.request.url
        url_part = urlparse(url)
        scheme = url_part.scheme
        host = scheme + '://' + request.get_header('host')
        request.HOST = host
        request.BASE_URL = add_trailing_slash(host) + remove_begining_slash(add_trailing_slash(base_url()))
    
    def serve_assets(self, path, application='index'):
        """ Serve static files
            There is no need to call this function manually
        """
        # return things
        APP_PATH = application_path()
        APP_PATH = remove_trailing_slash(APP_PATH)
        output = {}
        if os.path.exists(os.path.join(APP_PATH, application, "assets", path)):
            output = static_file(path, root=os.path.join(APP_PATH, application, "assets"))
        else:
            output = static_file(path, root=os.path.join(APP_PATH, application, "assets", "index"))
        return output

def isset(variable):
    """ PHP favoFore.RED isset. 
        Usage: isset("a_variable_name")
    """
    return variable in locals() or variable in globals()

def add_trailing_slash(string):
    """ Add trailing slash
    """
    if len(string)>0 and string[-1] != '/':
        string += '/'
    return string

def remove_trailing_slash(string):
    """ Remove trailing slash
    """
    if len(string)>0 and string[-1] == '/':
            string  = string[:-1]
    return string

def add_begining_slash(string):
    """ Add begining slash
    """
    if len(string)>0 and string[0] != '/':
        string = '/'+string
    return string

def remove_begining_slash(string):
    """ Remove begining slash
    """
    if len(string)>0 and string[0] == '/':
            string  = string[1:]
    return string

def runtime_path(path=''):
    if '__KOKOROPY_RUNTIME_PATH__' in os.environ:
        RUNTIME_PATH = os.environ['__KOKOROPY_RUNTIME_PATH__']
    else:
        RUNTIME_PATH = '.runtime/'
    return RUNTIME_PATH + remove_begining_slash(path)

def application_path(path=''):
    if '__KOKOROPY_APPLICATION_PATH__' in os.environ:
        APPLICATION_PATH = os.environ['__KOKOROPY_APPLICATION_PATH__']
    else:
        APPLICATION_PATH = './applications/'
    return APPLICATION_PATH + remove_begining_slash(path)

def application_package():
    if '__KOKOROPY_APPLICATION_PACKAGE__' in os.environ:
        APPLICATION_PACKAGE = os.environ['__KOKOROPY_APPLICATION_PACKAGE__']
    else:
        APPLICATION_PACKAGE = os.path.split(remove_trailing_slash(application_path()))[-1]
    return APPLICATION_PACKAGE

def base_url(url=''):
    if '__KOKOROPY_BASE_URL__' in os.environ:
        BASE_URL = os.environ['__KOKOROPY_BASE_URL__']
    else:
        BASE_URL = '/' 
    return BASE_URL + remove_begining_slash(url)  

def rmtree(path, ignore_errors=False, onerror=None):
    """ Alias for shutil.rmtree
        Normal usage:
            rmtree("/home/some_directory")
    """
    shutil.rmtree(path, ignore_errors, onerror)

def copytree(src, dst, symlinks=False, ignore=None):
    """ Enchancement of shutil.copytree
        Will really copy directory recursively.
        If dst is not exists, it will be created.
        If src is not exists, it will be ignoFore.RED without throwing any error
        Normal usage:
            copytree("source_directory", "destination_directory")
    """
    if os.path.exists(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d, symlinks, ignore)
            else:
                if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                    shutil.copy2(s, d)

def makedirs(directory, mode='0777'):
    os.makedirs(directory, mode)

def file_put_contents(filename, data):
    f = file(filename, 'w')
    f.write(data)
    f.close()

def file_get_contents(filename):
    if os.path.exists(filename):
        return ''.join(open(filename).readlines())
    else:
        return ''.join(urlopen(filename).readlines())

def _sort_names(names=[], key=None):
    """ Sort list or list of dictionary for routing
        When sort list of dictionary, the key must be defined.
        Sorting process based on element length reversed.
        If there is an "index" element, it will be put as the last element
        Usage:
            names = ["action_index", "action_play", "action_sleep", "action_eat"]
            print (sort_names(names))
            # will print ["action_sleep", "action_play", "action_eat", "action_index"]
            
            names = [
                {"function" : "action_index"}, {"function" : "action_play"}, 
                {"function" : "action_sleep"}, {"function" : "action_eat"}]
            print (sort_names(names))
            # will print [
                {"function" : "action_sleep"}, {"function" : "action_play"}, 
                {"function" : "action_eat"},   {"function" : "action_index"}]
    """
    index_exists = False
    index_obj = None
    # check and remove index object if it is exists
    for i in xrange(len(names)):
        # get identifier
        if key is None:
            identifier = names[i]
        else:
            identifier = names[i][key]
        # check identifier
        if identifier.split("_")[-1] ==  "index":
            index_obj = names[i]
            index_exists = True
        # exit from loop
        if index_exists:
            break
    if index_exists:
        names.remove(index_obj)
    #sort the other normal elements
    names.sort(key = len, reverse=True)
    # re-add index object if it is exists
    if index_exists:
        names.append(index_obj)
    # return
    return names

def _get_basic_routes(directory, controller, function):
    """ Get basic route string
        This will handle "index" stuff.
    """
    basic_routes = []
    # basic routes
    basic_routes.append(base_url("/".join((directory, controller, function))))
    if function == "index":
        basic_routes.append(base_url("/".join((directory, controller))))
    if controller == "index":
        basic_routes.append(base_url("/".join((directory, function))))
        if function == "index":
            basic_routes.append(base_url(directory))
    if directory == "index":
        basic_routes.append(base_url("/".join((controller, function))))
        if function == "index":
            basic_routes.append(base_url(controller))
        if controller == "index":
            basic_routes.append(base_url(function))
            if function == "index":
                basic_routes.append(base_url())
    # return
    return basic_routes

def _get_routes(directory, controller, function, parameters):
    """ Get complete route string
        This will handle parameters and automatically add trailing slash
    """
    basic_routes = _get_basic_routes(directory, controller, function)
    # parameter patterns
    parameter_patterns = []
    for parameter in parameters:
        parameter_patterns.append("<"+parameter+">")
    # complete routes
    routes = []
    for basic_route in basic_routes:
        for i in reversed(xrange(len(parameter_patterns))):
            parameter_segment = "/".join(parameter_patterns[:i+1])
            routes.append(basic_route+"/"+parameter_segment)
        routes.append(basic_route)
        if basic_route[-1] != "/":
            routes.append(basic_route+"/")
    # return
    return routes

def _publish_methods(directory, controller, prefix, methods=[], publishers=[]):
    """ Publish methods
        directory, controller, and prefix should be string
        methods should be list of tuple. The tuple should has 2 element. 
        The first one is function name, the second one is function object
        publishers should be list of routing methods
    """
    methods = _sort_names(methods, 0)
    for method in methods:
        method_name = str(method[0])
        method_object = method[1]
        name_segments = method_name.split("_")
        # ignore functions without prefix
        if not name_segments[0] == prefix:
            continue 
        method_published_name = "_".join(name_segments[1:])
        parameters = inspect.getargspec(method_object)[0][1:]
        routes = _get_routes(directory, controller, method_published_name, parameters)
        for single_route in routes:
            for publisher in publishers:
                publisher(single_route)(method_object)

def import_routes(route_location):
    # import route
    module_obj = None
    __import__(route_location, globals(), locals())
    module_obj = sys.modules[route_location]
    url_properties = {
            'urls' : ['GET', 'POST', 'PUT', 'DELETE'],
            'gets' : ['GET'],
            'posts': ['POST'],
            'puts' : ['PUT'],
            'deletes': ['DELETE']
        }
    # urls
    for url_property in url_properties:
        methods = url_properties[url_property]
        if hasattr(module_obj, url_property):
            for url_pair in module_obj.urls:
                slashed_url = add_trailing_slash(url_pair[0])
                unslashed_url = remove_trailing_slash(url_pair[0])
                route(slashed_url, methods, url_pair[1])
                route(unslashed_url, methods, url_pair[1])
    # hooks
    if hasattr(module_obj, 'hooks'):
        for hook_pair in module_obj.hooks:
            hook(hook_pair[0])(hook_pair[1])
    # errors
    if hasattr(module_obj, 'errors'):
        for error_pair in module_obj.errors:
            error(error_pair[0])(error_pair[1])
            
def _application_list():
    app_path = application_path()
    application_list = []
    for application in os.listdir(app_path):
        if os.path.isfile(os.path.join(app_path, application, "__init__.py")) and \
        os.path.isfile(os.path.join(app_path, application, "controllers", "__init__.py")):
            application_list.append(application)
    application_list = _sort_names(application_list)
    return application_list
    
def kokoro_init(**kwargs):
    """ Start a server instance. This method blocks until the server terminates.

        :param app: WSGI application or target string supported by
               :func:`load_app`. (default: :func:`default_app`)
        :param server: Server adapter to use. See :data:`server_names` keys
               for valid names or pass a :class:`ServerAdapter` subclass.
               (default: `wsgiref`)
        :param host: Server address to bind to. Pass ``0.0.0.0`` to listens on
               all interfaces including the external one. (default: 127.0.0.1)
        :param port: Server port to bind to. Values below 1024 require root
               privileges. (default: 8080)
        :param reloader: Start auto-reloading server? (default: False)
        :param interval: Auto-reloader interval in seconds (default: 1)
        :param quiet: Suppress output to stdout and stderr? (default: False)
        :param options: Options passed to the server adapter.
     """
    ###################################################################################################
    # kwargs arguments
    ###################################################################################################    
    APP                 = kwargs.pop("app",                 bottle.app()        )
    SERVER              = kwargs.pop("server",              "kokoro"            )
    DEBUG               = kwargs.pop("debug",               True                )
    PORT                = kwargs.pop("port",                8080                )
    RELOADER            = kwargs.pop("reloader",            True                )
    HOST                = kwargs.pop("host",                "127.0.0.1"         )
    QUIET               = kwargs.pop("quiet",               False               )
    INTERVAL            = kwargs.pop("interval",            1                   )
    PLUGINS             = kwargs.pop("plugins",             None                )
    RUN                 = kwargs.pop("run",                 True                )
    BASE_URL            = kwargs.pop("base_url",            '/'                 )
    RUNTIME_PATH        = kwargs.pop("runtime_path",        '.runtime/'         )
    ###################################################################################################
    # parameters
    ###################################################################################################
    APPLICATION_PATH                = add_trailing_slash(os.path.abspath('./applications'))
    BASE_URL                        = add_trailing_slash(add_begining_slash(BASE_URL))
    RUNTIME_PATH                    = add_trailing_slash(os.path.join(tempfile.gettempdir(), RUNTIME_PATH))
    UNTRAILED_SLASH_RUNTIME_PATH    = remove_trailing_slash(RUNTIME_PATH)
    APPLICATION_PACKAGE             = os.path.split(remove_trailing_slash(APPLICATION_PATH))[-1]
    MPL_CONFIG_DIR_PATH             = os.path.join(UNTRAILED_SLASH_RUNTIME_PATH,"mplconfigdir")
    # save BASE_URL and RUNTIME_PATH to os.environ
    os.environ['__KOKOROPY_BASE_URL__']         = BASE_URL
    os.environ['__KOKOROPY_RUNTIME_PATH__']     = RUNTIME_PATH
    os.environ['__KOKOROPY_APPLICATION_PATH__'] = APPLICATION_PATH
    ###################################################################################################
    # prepare runtime path
    ###################################################################################################
    print (Fore.YELLOW + 'Version : ' + Fore.BLUE + __version__ + Fore.RESET)
    print (Fore.YELLOW + "* Create Runtime Path : " + Fore.BLUE + UNTRAILED_SLASH_RUNTIME_PATH + Fore.RESET)
    if not os.path.exists(UNTRAILED_SLASH_RUNTIME_PATH):
        os.makedirs(UNTRAILED_SLASH_RUNTIME_PATH)
    if not os.path.exists(MPL_CONFIG_DIR_PATH):
        os.makedirs(MPL_CONFIG_DIR_PATH)
    # set mplconfigdir for matplotlib
    if ('MPLCONFIGDIR' not in os.environ) or (not os.access(os.environ['MPLCONFIGDIR'], os.W_OK)):
        os.environ['MPLCONFIGDIR'] = MPL_CONFIG_DIR_PATH # point MPLCONFIGDIR to writable directory   
    ###################################################################################################
    # get all kokoropy application
    ###################################################################################################
    # init application_list
    print (Fore.YELLOW + "* Detect Applications" + Fore.RESET)
    application_list = _application_list()
    ###################################################################################################
    # get application controller modules
    ###################################################################################################
    # controller_dict_list is a dictionary with application name as key 
    # and array of controller as value
    controller_dict_list = {}
    for application in application_list:
        for file_name in os.listdir(os.path.join(APPLICATION_PATH, application, "controllers")):
            # get application inside application"s controller
            file_name_segments = file_name.split(".")
            first_segment = file_name_segments[0]
            last_segment = file_name_segments[-1]
            if (first_segment == "__init__") or (not last_segment == "py"):
                continue
            module_name = inspect.getmodulename(file_name)
            if module_name is None:
                continue
            if not application in controller_dict_list:
                controller_dict_list[application] = []
            controller_dict_list[application].append(module_name)   
    ###################################################################################################
    # some pFore.REDefined routes
    ###################################################################################################
    application_pattern = "|".join(application_list)
    kokoro_router = _Kokoro_Router()
    route(base_url("<path:re:(favicon.ico)>"))(kokoro_router.serve_assets)    
    route(base_url("<application:re:"+application_pattern+">/assets/<path:re:.+>"))(kokoro_router.serve_assets)
    route(base_url("assets/<path:re:.+>"))(kokoro_router.serve_assets)
    hook('before_request')(kokoro_router.before_request)
    
    print(Fore.YELLOW + "* Register Global Routes" + Fore.RESET)
    import_routes(APPLICATION_PACKAGE + ".routes")
    ###################################################################################################
    # Load routes
    ###################################################################################################
    for application in application_list:
        if os.path.isfile(os.path.join(APPLICATION_PATH, application, "routes.py")):
            print(Fore.YELLOW + "* Register Routes : " + Fore.BLUE + application + Fore.RESET)
            import_routes(APPLICATION_PACKAGE + ".routes")
    ###################################################################################################
    # Load Autoroute inside controller modules
    ###################################################################################################
    for application in controller_dict_list:
        for controller in controller_dict_list[application]:
            print(Fore.YELLOW + "* Find Controller : "+ Fore.BLUE + application + ".controllers." + controller + Fore.RESET)
            # import our controllers
            module_obj = None
            import_location = APPLICATION_PACKAGE+"."+application+".controllers."+controller
            __import__(import_location, globals(), locals())
            module_obj = sys.modules[import_location]
            members = inspect.getmembers(module_obj, inspect.isclass)
            # determine if autoroute_controller exists
            autoroute_controller_found = False
            autoroute_controller_name  = "";
            Controller = None
            for member in members:
                # if find any descendant of Autoroute_Controller and not Autoroute_Controller itself
                if member[1] != Autoroute_Controller and issubclass(member[1], Autoroute_Controller):
                    autoroute_controller_found = True
                    autoroute_controller_name  = member[0]
                    Controller = member[1]
                    break
            # skip if there is no autoroute_controller
            if not autoroute_controller_found:
                continue
            # make an instance of Default_Controller
            autoroute_controller = Controller()            
            methods = inspect.getmembers(autoroute_controller, inspect.ismethod)
            # publish all methods with REST prefix (get, post, put and delete)
            _publish_methods(application, controller, "get",    methods, [get]              )
            _publish_methods(application, controller, "post",   methods, [post]             )
            _publish_methods(application, controller, "put",    methods, [put]              )
            _publish_methods(application, controller, "delete", methods, [delete]           )
            # publish all methods with action prefix
            _publish_methods(application, controller, "action", methods, [route, get, post,
                                                                          put, delete]      )
            print(Fore.YELLOW + "   Register Autoroute Controller : " + Fore.BLUE + 
                  autoroute_controller_name + Fore.RESET)
    ###################################################################################################
    # add template & assets path
    ###################################################################################################
    TEMPLATE_PATH.pop()
    TEMPLATE_PATH.pop()
    TEMPLATE_PATH.append(APPLICATION_PATH)
    ###################################################################################################
    # run the application
    ###################################################################################################
    session_opts = {
        "session.type": "file",
        "session.data_dir": os.path.join(UNTRAILED_SLASH_RUNTIME_PATH,"session"),
        "session.auto": True,
    }
    app = beaker.middleware.SessionMiddleware(APP, session_opts)
    port = int(os.environ.get("PORT", PORT))
    if RUN:
        if SERVER == 'kokoro':
            SERVER = KokoroWSGIRefServer(host=HOST, port=port)
        print(Fore.GREEN)
        run(app=app, server=SERVER, reloader=RELOADER, host=HOST, 
            port=port, quiet=QUIET, interval=INTERVAL, debug=DEBUG, plugins=PLUGINS, **kwargs)
        print(Fore.RESET)
    else:
        return app

def draw_matplotlib_figure(figure, file_name = None, application_name = 'index'):
    import pkgutil
    # import FigureCanvas
    matplotlib_found = False
    StringIO_found = False
    for iter_modules in pkgutil.iter_modules():
        module_name = iter_modules[1]
        if module_name == 'matplotlib':
            matplotlib_found = True
        if module_name == 'StringIO':
            import StringIO
            StringIO_found = True
    if matplotlib_found and StringIO_found:
        if file_name is None:
            # return png output
            from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
            canvas = FigureCanvas(figure)
            png_output = StringIO.StringIO()
            canvas.print_png(png_output)
            response.content_type = 'image/png'
            return png_output.getvalue()
        else:
            file_path = _asset_path(file_name, application_name)
            figure.savefig(file_path, dpi=100)
            return base_url(application_name+'/assets/'+file_name)
    else:
        return False

def _asset_path(path, application_name):
    ''' return asset path
    '''
    return application_path(os.path.join(application_name, 'assets', path))

def save_uploaded_asset(upload_key_name, path='', application_name='index'):
    upload =  request.files.get(upload_key_name)
    if upload is None:
        return False
    else:
        file_name = upload.filename
        remove_asset(os.path.join(path, file_name), application_name)
        # appends upload.filename automatically
        upload_path = _asset_path(path, application_name)
        upload.save(upload_path)
        return True

def remove_asset(path, application_name='index'):
    asset_path = _asset_path(path, application_name)
    try:
        os.remove(asset_path)
        return True
    except OSError:
        return False

def _migration_connection_string(application_name):
    return 'sqlite:///'+application_path(os.path.join(application_name, 'db','__migration.db'))

def _migration_session(application_name):
    engine = create_engine(_migration_connection_string(application_name), echo=False)
    # create db session
    db_session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(bind=engine)
    return db_session

def migration_log(application_name=None):
    if application_name is None:
        # get application_list and sort it by name
        application_list = _application_list()
        # migration list
        migrations = {}
        for application_name in application_list:
            migrations[application_name] = migration_log(application_name)
        return migrations
    else:
        db_session = _migration_session(application_name)
        return db_session.query(Migration).order_by(desc(Migration.signature)).all()

def _migration_max(application_name):
    db_session = _migration_session(application_name)
    return db_session.query(Migration).order_by(desc(Migration.signature)).first()

def migration_upgrade(application_name=None, migration_name=None):
    if application_name is None:
        # get application_list and sort it by name
        application_list = _application_list()
        # do migration
        for application_name in application_list:
            migration_upgrade(application_name)
    elif migration_name is None:
        # get migration list and sort it by name
        migration_log = []
        for migration_name in os.listdir(application_path(os.path.join(application_name, 'migrations'))):
            file_name, extension = os.path.splitext(migration_name)
            if extension == '.py' and file_name != '__init__':
                migration_log.append(file_name)
        migration_log = _sort_names(migration_log)
        # do migration
        for migration_name in migration_log:
            print (application_name, migration_name)
            migration_upgrade(application_name, migration_name)
    else:
        application_package = os.path.split(remove_trailing_slash(application_path()))[-1]
        module_obj = None
        import_location = application_package + "." + application_name + ".migrations." + migration_name
        __import__(import_location, globals(), locals())
        module_obj = sys.modules[import_location]
        # get max_signature from database
        max_migration = _migration_max(application_name)
        if max_migration is None:
            max_signature = ''
        else:
            max_signature = max_migration.signature
        # define session
        db_session = _migration_session(application_name)
        if hasattr(module_obj, 'upgrade'):
            signature = module_obj.signature
            if signature > max_signature:
                module_obj.upgrade()
                # save the new migration
                new_migration = Migration(signature, migration_name)
                db_session.add(new_migration)
                db_session.commit()

def migration_downgrade(application_name):
    # get max migration
    max_migration = _migration_max(application_name)
    migration_name = max_migration.migration_name
    # look for migration script
    application_package = os.path.split(remove_trailing_slash(application_path()))[-1]
    module_obj = None
    import_location = application_package + "." + application_name + ".migrations." + migration_name
    __import__(import_location, globals(), locals())
    module_obj = sys.modules[import_location]
    if hasattr(module_obj, 'downgrade'):
        module_obj.downgrade()
        # define session
        db_session = _migration_session(application_name)
        # remove max migration
        db_session.delete(max_migration)
        db_session.commit()

def make_timestamp():
    return datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

def scaffold_application(application_name):
    source = os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_application')
    destination = application_path(application_name)
    copytree(source, destination)

def scaffold_migration(application_name, migration_name, table_name='your_table', *columns):
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_migration.py'))
    timestamp = make_timestamp()
    # make timestamp
    content = content.replace('g_timestamp', timestamp)
    # make add column and drop column scripts
    add_column_scripts = []
    drop_column_scripts = []
    for column in columns:
        column = column.split(':')
        if len(column)>1:
            coltype= column[1]
            column = column[0]
        else:
            coltype = 'String'
            column = column[0]
        add_column_scripts.append('op.add_column(\'%s\', Column(\'%s\', %s))' % (table_name, column, coltype))
        drop_column_scripts.append('op.drop_column(\'%s\', \'%s\')' % (table_name, column))
    add_column_scripts = '\n    '.join(add_column_scripts)
    drop_column_scripts = '\n    '.join(drop_column_scripts)
    content = content.replace('# g_add_column', add_column_scripts)
    content = content.replace('# g_drop_column', drop_column_scripts)
    # make application if not exists
    if not os.path.exists(application_path(application_name)):
        scaffold_application(application_name)
    # determine file name
    filename = timestamp+'_'+migration_name+'.py'
    filename = application_path(os.path.join(application_name, 'migrations', filename))
    # write file
    file_put_contents(filename, content)

def add_to_structure(structure, table_name, column_name = None, content = None):
    '''
    return new column_name
    '''
    if table_name not in structure:
        structure[table_name] = {}
    if column_name is not None:
        if column_name in structure[table_name]:
            i = 1
            while column_name + '_' + str(i) in table_name:
                i += 1
            column_name = column_name + '_' + str(i)
        if content is None:
            content = 'Column(String)'
        structure[table_name][column_name] = content
    return column_name

def _structure_to_script(structure):
    '''
    example of data structure:
        structure = [
            'nerd' = {
                'name' : 'Column(String)',
                'address' : 'Column(String)'
            },
            'os' = {
                'name' : 'Column(String)',
                'version' : 'Column(String)'
            }
        ]
    '''
    script = ''
    for table_name in sorted(structure):
        ucase_table_name = table_name.title()
        script += 'class ' + ucase_table_name + '(Model):\n'
        script += '    __session__ = session\n'
        for column_name in sorted(structure[table_name]):
            content = structure[table_name][column_name]
            script += '    ' + column_name + ' = ' + content + '\n'
        script += '\n'
    return script

def scaffold_model(application_name, table_name, *columns):
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_model.py'))
    # define structure
    ucase_table_name = table_name.title()
    structure = {}
    for column in columns:
        column = column.split(':')
        if len(column)>2:
            colname = column[0]
            other_table_name = column[1]
            relationship = column[2]
            ucase_other_table_name = other_table_name.title()
            if relationship == 'onetomany' or relationship == 'one_to_many':
                # other table
                add_to_structure(structure, other_table_name)
                # foreign key
                coltype = 'Column(Integer, ForeignKey("' + table_name + '._real_id"))'
                fk_col_name = '_' + table_name + '_real_id'
                fk_col_name = add_to_structure(structure, other_table_name, fk_col_name, coltype)
                # relationship
                coltype = 'relationship("' + ucase_other_table_name + '", foreign_keys="' + ucase_other_table_name + '.' + fk_col_name + '")'
                add_to_structure(structure, table_name, colname, coltype)
            elif relationship == 'manytoone' or relationship == 'many_to_one':
                # other table
                add_to_structure(structure, other_table_name)
                # foreign key
                coltype = 'Column(Integer, ForeignKey("' + other_table_name + '._real_id"))'
                fk_col_name = '_' + other_table_name + '_real_id'
                fk_col_name = add_to_structure(structure, table_name, fk_col_name, coltype)
                # relationship
                coltype = 'relationship("' + ucase_other_table_name + '", foreign_keys="' + ucase_table_name + '.' + fk_col_name + '")'
                add_to_structure(structure, table_name, colname, coltype)
        else:
            colname = column[0]
            if len(column)>1:
                coltype = column[1]
            else:
                coltype = 'String'
            add_to_structure(structure, table_name, colname, 'Column('+coltype+')')
    # replace content
    content = content.replace('# g_structure', _structure_to_script(structure))
    # make application if not exists
    if not os.path.exists(application_path(application_name)):
        scaffold_application(application_name)
    # determine file name
    filename = table_name+'.py'
    filename = application_path(os.path.join(application_name, 'models', filename))
    # write file
    file_put_contents(filename, content)

def scaffold_crud(application_name, table_name, *columns):
    scaffold_model(application_name, table_name, *columns)
    ucase_table_name = table_name.title()
    
    # controller
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_controller.py'))    
    content = content.replace('G_Table_Name', ucase_table_name)
    content = content.replace('g_table_name', table_name)
    content = content.replace('g_application_name', application_name)
    filename = table_name+'.py'
    filename = application_path(os.path.join(application_name, 'controllers', filename))
    # write file
    file_put_contents(filename, content)
    
    # view
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_view_list.html'))    
    content = content.replace('G_Table_Name', ucase_table_name)
    content = content.replace('g_table_name', table_name)
    content = content.replace('g_application_name', application_name)
    filename = table_name+'_list.html'
    filename = application_path(os.path.join(application_name, 'views', filename))
    # write file
    file_put_contents(filename, content)