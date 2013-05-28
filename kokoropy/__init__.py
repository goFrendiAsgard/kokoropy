# -*- coding: utf-8 -*-

###################################################################################################
# Add this directory to sys.path
###################################################################################################
import os, inspect, sys, shutil
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

###################################################################################################
# Import things
###################################################################################################
import bottle, sqlalchemy, beaker, threading, time
import beaker.middleware
from bottle import default_app, debug, run, static_file,\
    request, TEMPLATE_PATH, template, route, get, post, put, delete, error, hook, Bottle

###################################################################################################
# Hacks & Dirty Tricks :)
###################################################################################################  
# Python 3 hack for xrange
if sys.version_info >= (3,0,0):
    xrange = range
# Intellisense hack
if 0:
    request.SESSION = []
    
###################################################################################################
# KokoroWSGIRefServer
###################################################################################################
class KokoroWSGIRefServer(bottle.ServerAdapter):
    def __int__(self, *args, **kwargs):
        super(bottle.ServerAdapter, self).__init__(*args, **kwargs)
        self.srv = None

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
@hook("before_request")
def _before_request():
    """ Before request event
        Inject request.SESSION as alias of request.environ["beaker.session"]
        There is no need to call this function manually
    """
    request.SESSION = request.environ["beaker.session"]

@route("/<path:re:(favicon.ico)>")
@route("/assets/<path:re:.+>")
def _serve_assets(path):
    """ Serve static files
        There is no need to call this function manually
    """
    if os.path.exists(os.path.join(".runtime", "assets", path)):
        return static_file(path, root=os.path.join(".runtime", "assets"))
    else:
        return static_file(path, root=os.path.join(".runtime", "assets", "index"))

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
        If src is not exists, it will be ignored without throwing any error
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
    basic_routes.append("/"+directory+"/"+controller+"/"+function)
    if function == "index":
        basic_routes.append("/"+directory+"/"+controller)
    if controller == "index":
        basic_routes.append("/"+directory+"/"+function)
        if function == "index":
            basic_routes.append("/"+directory)            
    if directory == "index":
        basic_routes.append("/"+controller+"/"+function)
        if function == "index":
            basic_routes.append("/"+controller)
        if controller == "index":
            basic_routes.append("/"+function)
            if function == "index":
                basic_routes.append("")
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
    APPLICATION_PATH    = kwargs.pop("application_path",    "./applications"    )
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
    ###################################################################################################
    # parameters
    ###################################################################################################
    APPLICATION_PACKAGE = os.path.split(APPLICATION_PATH)[-1]
    CURRENT_PATH        = os.path.split(APPLICATION_PATH)[0]
    RUNTIME_PATH        = os.path.join(CURRENT_PATH,".runtime")
    ###################################################################################################
    # prepare runtime path
    ###################################################################################################
    print ("PREPARE RUNTIME PATH")
    if not os.path.exists(RUNTIME_PATH):
        os.makedirs(RUNTIME_PATH)
    ###################################################################################################
    # get all kokoropy module directory_list
    ###################################################################################################
    # init directory_list
    print ("INIT APPLICATION DIRECTORIES")
    directory_list = []
    for directory in os.listdir(APPLICATION_PATH):
        if os.path.isfile(os.path.join(APPLICATION_PATH, directory, "__init__.py")) and \
        os.path.isfile(os.path.join(APPLICATION_PATH, directory, "controllers", "__init__.py")):
            directory_list.append(directory)
    directory_list = _sort_names(directory_list)    
    ###################################################################################################
    # get directory controller modules
    ###################################################################################################
    # controller_module_directory_list is a dictionary with directory name as key 
    # and array of controller as value
    controller_module_directory_list = {}
    for directory in directory_list:
        for file_name in os.listdir(APPLICATION_PATH+"/"+directory+"/controllers"):
            # get module inside directory"s controller
            file_name_segments = file_name.split(".")
            first_segment = file_name_segments[0]
            last_segment = file_name_segments[-1]
            if (first_segment == "__init__") or (not last_segment == "py"):
                continue
            module_name = inspect.getmodulename(file_name)
            if module_name is None:
                continue
            if not directory in controller_module_directory_list:
                controller_module_directory_list[directory] = []
            controller_module_directory_list[directory].append(module_name)    
    ###################################################################################################
    # Load everything inside controller modules
    ###################################################################################################
    exec("import "+APPLICATION_PACKAGE)
    for directory in controller_module_directory_list:
        for controller_module in controller_module_directory_list[directory]:
            # load everything inside the controllers
            print("LOAD CONTROLLER : "+controller_module)
            exec("from "+APPLICATION_PACKAGE+"."+directory+".controllers."+controller_module+" import *")                
    ###################################################################################################
    # Load Default_Controller inside controller modules
    ###################################################################################################
    for directory in controller_module_directory_list:
        for controller_module in controller_module_directory_list[directory]:
            module_obj = None
            exec("import "+APPLICATION_PACKAGE+"."+directory+".controllers."+controller_module+" as module_obj")
            members = inspect.getmembers(module_obj, inspect.isclass)
            # determine if default_controller exists
            default_controller_found = False
            Default_Controller = None
            for member in members:
                if member[0] == "Default_Controller":
                    default_controller_found = True
                    Default_Controller = member[1]
                    break
            # skip if there is no default_controller
            if not default_controller_found:
                continue
            # make an instance of Default_Controller
            default_controller = Default_Controller()            
            methods = inspect.getmembers(default_controller, inspect.ismethod)
            # publish all methods with REST prefix (get, post, put and delete)
            _publish_methods(directory, controller_module, "act_get",    methods, [get]              )
            _publish_methods(directory, controller_module, "act_post",   methods, [post]             )
            _publish_methods(directory, controller_module, "act_put",    methods, [put]              )
            _publish_methods(directory, controller_module, "act_delete", methods, [delete]           )
            # publish all methods with action prefix
            _publish_methods(directory, controller_module, "action", methods, [route, get, post, 
                                                                               put, delete]      )
    ###################################################################################################
    # add template & assets path
    ###################################################################################################
    global_view_path = os.path.join(RUNTIME_PATH, "views")
    global_asset_path = os.path.join(RUNTIME_PATH, "assets")
    rmtree(global_view_path)
    rmtree(global_asset_path)
    # application"s assets & views
    for directory in directory_list:
        print("REGISTER TEMPLATE PATH : "+directory+"/views/")
        old_path = os.path.join(APPLICATION_PATH, directory, "views")
        app_view_path = os.path.join(global_view_path, directory)
        copytree(old_path, app_view_path)
        print("REGISTER ASSETS PATH : "+directory+"/assets/")
        old_path = os.path.join(APPLICATION_PATH, directory, "assets")
        app_asset_path = os.path.join(global_asset_path, directory)
        copytree(old_path, app_asset_path)
    # register template path
    TEMPLATE_PATH.append(global_view_path)
    ###################################################################################################
    # run the application
    ###################################################################################################
    session_opts = {
        "session.type": "file",
        "session.data_dir": os.path.join(RUNTIME_PATH,"session"),
        "session.auto": True,
    }
    app = beaker.middleware.SessionMiddleware(APP, session_opts)
    port = int(os.environ.get("PORT", PORT))
    if RUN:
        if SERVER == 'kokoro':
            SERVER = KokoroWSGIRefServer(host=HOST, port=port)
        run(app=app, server=SERVER, reloader=RELOADER, host=HOST, 
            port=port, quiet=QUIET, interval=INTERVAL, debug=DEBUG, plugins=PLUGINS, **kwargs)
    else:
        return app