#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '0.0.0'
###################################################################################################
# Add package directory to sys.path
###################################################################################################
import os, inspect, sys, shutil, time
from datetime import datetime
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(__file__),'packages'))

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

###################################################################################################
# Import things
###################################################################################################
import bottle, tempfile, re, beaker.middleware, types
from bottle import default_app, debug, run, static_file,\
    response, request, TEMPLATE_PATH, route, get,\
    post, put, delete, error, hook, Bottle, redirect

from bottle import template as _bottle_template

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import desc

# colorama
from colorama import init, Fore, Back, Style
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
        
# intellisense hack
request.SESSION = {}

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

###################################################################################################
# Commonly used functions
###################################################################################################

def isset(variable):
    """ PHP favoured isset. 
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

def makedirs(directory, mode=0777):
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

def _key_spaces(data):
    spaces = {}
    max_len = 0
    for item in data:
        if len(item)>max_len:
            max_len = len(item)
    for item in data:
        spaces[item] = ' ' * (max_len - len(item))
    return spaces

def _type_label(type_label, mode = 'plain'):
    type_label = str(type_label)
    # strip out '<' and '>'
    if type_label[0] == '<':
        type_label = type_label[1:]
    if type_label[-1] == '>':
        type_label = type_label[:-1]
    # determine return base on mode
    if mode == 'html':
        return '<i>&lt;' + type_label + '&gt;</i>'
    elif mode == 'console':
        return Fore.YELLOW + Style.DIM + type_label + Style.NORMAL + Fore.RESET
    else:
        return '<' + type_label + '>'

def _key_label(key, mode = 'plain'):
    key = str(key)
    # determine return base on mode
    if mode == 'html':
        return '<b>' + key + '</b>'
    elif mode == 'console':
        return Fore.YELLOW + Style.BRIGHT + key + Style.NORMAL + Fore.RESET
    else:
        return key

def _value_label(value, mode = 'plain'):
    if type(value) == types.StringType:
        value = "'" + value + "'"
    else:
        value = str(value)
    # determine return base on mode
    if mode == 'html':
        return '<b>' + value + '</b>'
    elif mode == 'console':
        return Fore.CYAN + Style.BRIGHT + value + Style.NORMAL + Fore.RESET
    else:
        return value

def _var_dump(variable, depth = 0, not_new_line = False, mode = 'plain'):
    indentation   = " " * 4
    padding       = indentation * depth
    key_padding   = indentation * (depth+1)
    first_padding = '' if not_new_line else padding
    not_new_line  = True
    depth+= 1
    # Dictionary
    if type(variable) == types.DictType :
        items = []
        spaces = _key_spaces(variable)
        for key in variable :
            item = key_padding + "%s%s : %s" % (_key_label("'"+key+"'",mode), spaces[key], _var_dump(variable[key], depth, True, mode))
            items.append(item)
        items = ',\n'.join(items)
        return '%s%s {\n%s\n%s}' % ( first_padding, _type_label('Dictionary', mode), items, padding)
    # Instance of class
    elif type(variable) == types.InstanceType:
        items = []
        spaces = _key_spaces(dir(variable))
        for key in dir(variable):
            item = key_padding + "%s%s : %s" % (_key_label(key,mode), spaces[key], _var_dump(getattr(variable,key), depth, True, mode))
            items.append(item)
        items = ',\n'.join(items)
        return '%s%s (\n%s\n%s)' % ( first_padding, _type_label('Instance of ' + str(variable.__class__), mode), items, padding)
    # List
    elif type(variable) == types.ListType :
        items = []
        for item in variable :
            items.append(_var_dump(item, depth, False, mode))
        items = ',\n'.join(items)
        return '%s%s [\n%s\n%s]' % ( first_padding, _type_label('List', mode), items, padding)
    # Tuple
    elif type(variable) == types.TupleType :
        items = []
        for item in variable :
            items.append(_var_dump(item, depth, False, mode))
        items = ',\n'.join(items)
        return '%s%s (\n%s\n%s)' % ( first_padding, _type_label('Tuple', mode), items, padding)
    elif type(variable) == types.MethodType:
        return first_padding + _type_label('Method', mode)
    elif type(variable) == types.FunctionType:
        return first_padding + _type_label('Function', mode)
    elif type(variable) == types.BuiltinFunctionType:
        return first_padding + _type_label('BuiltinFunction', mode)
    elif type(variable) == types.BuiltinMethodType:
        return first_padding + _type_label('BuiltinMethod', mode)
    elif type(variable) == types.NoneType:
        return first_padding + _type_label('None', mode)
    elif type(variable) == types.ClassType:
        return first_padding + _type_label('Class', mode)
    elif type(variable) == types.BufferType:
        return first_padding + _type_label('Buffer', mode)
    elif type(variable) == types.TypeType:
        return first_padding + _type_label('Type', mode)
    elif type(variable) == types.ModuleType:
        return first_padding + _type_label('Module', mode)
    elif type(variable) == types.ObjectType:
        return first_padding + _type_label('Object', mode)
    elif type(variable) == types.StringType:
        return first_padding + _type_label('String', mode) + ' ' + _value_label(variable, mode)
    elif type(variable) == types.IntType:
        return first_padding + _type_label('Integer', mode) + ' ' + _value_label(variable, mode)
    elif type(variable) == types.LongType:
        return first_padding + _type_label('Long', mode) + ' ' + _value_label(variable, mode)
    elif type(variable) == types.FloatType:
        return first_padding + _type_label('Float', mode) + ' ' + _value_label(variable, mode)
    elif type(variable) == types.BooleanType:
        return first_padding + _type_label('Boolean', mode) + ' ' + _value_label(variable, mode)
    else:
        return first_padding + _type_label(type(variable), mode)

def var_dump(variable = None, **kwargs):
    if variable is None:
        variable = {'globals()' : globals(), 'locals()' : locals()}
    print_output = kwargs.pop('print_output', False)
    mode         = kwargs.pop('mode', 'plain')
    result       = _var_dump(variable, 0, False, mode)
    if mode == 'html':
        result = '<pre>' + result + '</pre>'
    if print_output:
        print(result)
    return result

###################################################################################################
# View & Template related functions
###################################################################################################
# load view
def load_view(application_name, *args, **kwargs):
    ''' Usage:
    load_view('application_name', 'view_name', ....)
    load_view('application_name/view_name', ....)
    '''
    # determine view_path
    if '/' in application_name:
        # if application_name has '/', then view_name is mean to be the first element of args
        view_path = application_name
    else:
        view_name = args[0]
        args = args[1:]
        view_path = os.path.join(application_name , "views" , view_name)
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
    return load_template(content, *args, **kwargs)

def load_template(template, *args, **kwargs):
    import_asset = '% from kokoropy.asset import JQUI_BOOTSTRAP_STYLE, JQUI_BOOTSTRAP_SCRIPT, KOKORO_CRUD_STYLE, KOKORO_CRUD_SCRIPT, HTML'
    # modify kwargs
    if 'BASE_URL' in request and request.BASE_URL is not None:
        kwargs['BASE_URL']  = request.BASE_URL
    else:
        kwargs['BASE_URL']  = base_url()
    kwargs['RUNTIME_PATH']  = runtime_path()
    kwargs['APP_PATH']      = application_path()
    kwargs['REQUEST']       = request
    # modify args
    args_list = list(args)
    # add \n to prevent template rendered as path
    if not '\n' in template:
        template = template + '\n'
    template = import_asset  + '\n'+ template
    # create block pattern
    block_pattern = r'{%( *)block( *)([A-Za-z0-9_-]*)( *)%}((.|\n)*?){%( *)endblock( *)%}+?'
    # get block_chunks
    block_chunks = re.findall(block_pattern, template)
    # remove all literal block from template
    template = re.sub(block_pattern, r'', template)
    # get template by rendering content
    args_list.insert(0, template)
    args = tuple(args_list)
    template = _bottle_template(*args, **kwargs)
    for chunk in block_chunks:
        block_name = chunk[2]
        block_content = chunk[4]
        # change {% parent %} into % __base_block_BLOCKNAME()\n
        block_content = re.sub(r'{%( *)parent( *)%}+?',
                               r'\n% __base_block_'+block_name+'()\n',
                               block_content)
        template = '\n% def __block_' + block_name + '():\n' + import_asset + '\n' + block_content + '\n% end\n' + template
    # change 
    #    {% block X %}Y{% endblock %}" 
    # into 
    #     % def __base_block_X:
    #         Y
    #     % end
    #     % setdefault('__block_X', __base_block_X)
    #     % __block_X()
    template = re.sub(block_pattern, 
                     r'\n% def __base_block_\3():\n' + import_asset + r'\n\5\n% end\n% setdefault("__block_\3", __base_block_\3)\n%__block_\3()\n',
                     template)
    # render again
    args_list[0] = template
    args = tuple(args_list)
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
            default_root = os.path.join(os.path.dirname(__file__),'statics')
            output = static_file(path, root=default_root)
        return output


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
        if prefix == '':
            method_published_name = method_name
        else:
            name_segments = method_name.split("_")
            # ignore functions without prefix
            if name_segments[0] != prefix:
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
            for url_pair in getattr(module_obj, url_property):
                # address               
                route_address = url_pair[0]
                slashed_url = add_begining_slash(add_trailing_slash(route_address))
                unslashed_url = add_begining_slash(remove_trailing_slash(route_address))
                # callback
                if len(url_pair)==1:
                    route_callback = 'Undefined callback'
                else:
                    route_callback = url_pair[1]
                if isinstance(route_callback, str):
                    content = route_callback
                    def wrapper():
                        return content
                    route_callback = wrapper
                # default values
                name, apply_, skip, configs = None, None, None, {}
                # name
                if len(url_pair)>2:
                    name = url_pair[2]
                    # apply
                    if len(url_pair)>3:
                        apply_ = url_pair[3]
                        # skip
                        if len(url_pair)>4:
                            skip = url_pair[4]
                            # configs
                            if len(url_pair)>5:
                                configs = url_pair[5]
                # call the routes
                route(slashed_url, methods, route_callback, name, apply_, skip, **configs)
                route(unslashed_url, methods, route_callback, name, apply_, skip, **configs)
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
    model_dict_list = {}
    for application in application_list:
        for file_name in os.listdir(os.path.join(APPLICATION_PATH, application, "controllers")):
            # get application inside application's controller
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
    # some predefined routes
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
            import_routes(APPLICATION_PACKAGE + "." + application + ".routes")
    ###################################################################################################
    # Load models
    ###################################################################################################
    for application in application_list:
        for file_name in os.listdir(os.path.join(APPLICATION_PATH, application, "models")):
            # get application inside application's model
            file_name_segments = file_name.split(".")
            first_segment = file_name_segments[0]
            last_segment = file_name_segments[-1]
            if (first_segment == "__init__") or (not last_segment == "py"):
                continue
            module_name = inspect.getmodulename(file_name)
            print(Fore.YELLOW + "* Find Model : "+ Fore.BLUE + application + ".models." + module_name + Fore.RESET)
            __import__(APPLICATION_PACKAGE+'.'+application+'.models.'+module_name, globals(), locals())
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

def publish_methods(directory, controller, methods=[], publishers=[route, get, post, put, delete]):
    _publish_methods(directory, controller, '', methods, publishers)

