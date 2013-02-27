#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################################################
# import "standard" modules (Please leave it as is)
########################################################################################################
import os, inspect
from application import app
from kokoropy.bottle import debug, run, static_file, TEMPLATE_PATH, template
custom_404, custom_403, custom_500 = None, None, None

########################################################################################################
# CONFIGURATION (Feel free to modify it)
########################################################################################################
HOST                = 'localhost'
PORT                = 8080
DEBUG               = True
RELOADER            = False

# Custom error handlers. Yes you can modify it (with care)
# But please let the function name as is

def custom_404(error):
    import random
    error_messages = [
        'Sorry, but there is no such a gray elephant in Atlantic...',
        'Are you sure that the page should be here? Well, in this case you are wrong',
        'Has you correctly write the URL?',
        'Go home you are drunk !!!',
        'It is not here, not here, not here... How many time should I tell you?',
        'Want the page to be exists? Hire us, and we will make one for you...',
        'Why do you look for something never exists? Please be realistic',
    ]
    message_index = random.randrange(0,len(error_messages))
    error_message = error_messages[message_index]
    data = {
       'error_title'  : '404, Page not found',
       'error_message' : error_message
    }
    return template('example/error', data = data)

def custom_403(error):
    import random
    error_messages = [
        'You are not authorized to enter ladies rest room, go out....',
        'You have landed at area 51. The MIB told us to not show the page',
        'Try to hack our site? We have record your IP Address and everything else',
        'What do you do here? Leave or die...',
    ]
    message_index = random.randrange(0,len(error_messages))
    error_message = error_messages[message_index]
    data = {
       'error_title'  : '403, Forbidden',
       'error_message' : error_message
    }
    return template('example/error', data = data)

def custom_500(error):
    import random
    error_messages = [
        'Right, right... It\'s not your fault it is our mistake',
        'Ouch,.. you have burn our hardisks. Be careful with what you click',
        'Do you notice that everytime you make our server error, a newborn baby will die...',
        'No no no... Not again...',
        'It is not our mistake, we have detect a bunch of ETI hacking our site',
    ]
    message_index = random.randrange(0,len(error_messages))
    error_message = error_messages[message_index]
    data = {
       'error_title'  : '500, Internal Server Error',
       'error_message' : error_message
    }
    return template('example/error', data = data)



########################################################################################################
# USER CONFIGURATION STOPPED HERE
# KOKOROPY BOOTSTRAP BEGINS HERE
#   And here is the dragon: 
#
#
#                                                  .~))>>
#                                                 .~)>>
#                                               .~))))>>>
#                                             .~))>>             ___
#                                           .~))>>)))>>      .-~))>>
#                                         .~)))))>>       .-~))>>)>
#                                       .~)))>>))))>>  .-~)>>)>
#                   )                 .~))>>))))>>  .-~)))))>>)>
#                ( )@@*)             //)>))))))  .-~))))>>)>
#             ).@(@@               //))>>))) .-~))>>)))))>>)>
#            (( @.@).              //))))) .-~)>>)))))>>)>
#          ))  )@@*.@@ )          //)>))) //))))))>>))))>>)>
#       ((  ((@@@.@@             |/))))) //)))))>>)))>>)>
#      )) @@*. )@@ )   (\_(\-\b  |))>)) //)))>>)))))))>>)>
#    (( @@@(.@(@ .    _/`-`  ~|b |>))) //)>>)))))))>>)>
#     )* @@@ )@*     (@)  (@) /\b|))) //))))))>>))))>>
#   (( @. )@( @ .   _/  /    /  \b)) //))>>)))))>>>_._
#    )@@ (@@*)@@.  (6///6)- / ^  \b)//))))))>>)))>>   ~~-.
# ( @jgs@@. @@@.*@_ VvvvvV//  ^  \b/)>>))))>>      _.     `bb
#  ((@@ @@@*.(@@ . - | o |' \ (  ^   \b)))>>        .'       b`,
#   ((@@).*@@ )@ )   \^^^/  ((   ^  ~)_        \  /           b `,
#     (@@. (@@ ).     `-'   (((   ^    `\ \ \ \ \|             b  `.
#       (*.@*              / ((((        \| | |  \       .       b `.
#                         / / (((((  \    \ /  _.-~\     Y,      b  ;
#                        / / / (((((( \    \.-~   _.`" _.-~`,    b  ;
#                       /   /   `(((((()    )    (((((~      `,  b  ;
#                     _/  _/      `"""/   /'                  ; b   ;
#                 _.-~_.-~           /  /'                _.'~bb _.'
#               ((((~~              / /'              _.'~bb.--~
#                                  ((((          __.-~bb.-~
#  ( This dragon also guards "laravel" realms ) .'  b .~~
#  ( Make sure you know what you do )          :bb ,' 
#  ( Or you will have a serious trouble )      ~~~~
#
########################################################################################################

# python 3 hack for xrange
try:
    xrange
except NameError:
    xrange = range

def sort_names(names=[], key=None):
    index_exists, empty_exists  = False, False
    index_obj, empty_obj        = None, None
    index_identifier = ['index', 'action_index']
    empty_identifier = ['', 'action', 'action_']
    # remove some special element
    for i in xrange(len(names)):
        # get identifier
        if key is None:
            identifier = names[i]
        else:
            identifier = names[i][key]
        # check identifier
        if identifier in index_identifier:
            index_obj = names[i]
            index_exists = True
        if identifier in empty_identifier:
            empty_obj = names[i]
            empty_exists = True
        # exit from loop
        if index_exists and empty_exists:
            break
    if index_exists:
        names.remove(index_obj)
    if empty_exists:
        names.remove(empty_obj)
    #sort the other normal elements
    names.sort(key = len, reverse=True)    
    # re add those removed special element
    if index_exists:
        names.append(index_obj)
    if empty_exists:
        names.append(empty_obj)
    # return
    return names

def get_basic_routes(directory, controller, function):
    basic_routes = []    
    # basic routes    
    if not function == '':
        basic_routes.append('/'+directory+'/'+controller+'/'+function)
    if function == '' or function == 'index':
        basic_routes.append('/'+directory+'/'+controller)
    if controller == '' or controller == 'index':
        if not function == '':
            basic_routes.append('/'+directory+'/'+function)
        if function == '' or function == 'index':
            basic_routes.append('/'+directory)            
    if directory == '' or directory == 'index':
        if not controller == '':
            if not function == '':
                basic_routes.append('/'+controller+'/'+function)
            if function == '' or function == 'index':
                basic_routes.append('/'+controller)
        if controller == '' or controller == 'index':
            if function != '':
                basic_routes.append('/'+function)
            if function == '' or function == 'index':
                basic_routes.append('')
    # return basic routes
    return basic_routes

def get_routes(directory, controller, function, parameters):
    basic_routes = get_basic_routes(directory, controller, function)    
    # parameter patterns
    parameter_patterns = []
    for parameter in parameters:
        parameter_patterns.append('<'+parameter+'>')
    # complete routes
    routes = []
    for basic_route in basic_routes:
        for i in reversed(xrange(len(parameter_patterns))):
            parameter_segment = "/".join(parameter_patterns[:i+1])
            routes.append(basic_route+'/'+parameter_segment)
        routes.append(basic_route)
        routes.append(basic_route+'/')
    # return routes
    return routes    


if __name__ == '__main__':
    # set debug mode
    debug(DEBUG)
    
    TEMPLATE_PATH.remove('./views/')
    
    ###################################################################################################
    # Define custom error handler
    ###################################################################################################
    if inspect.isfunction(custom_404) and inspect.isfunction(custom_403) and \
    inspect.isfunction(custom_500):
        error_handler = {
            404 : custom_404,
            403 : custom_403,
            500 : custom_500
        }    
        app.error_handler = error_handler
    
    # init directories
    print ('INIT APPLICATION DIRECTORIES')
    ###################################################################################################
    # get all kokoropy module directories
    ###################################################################################################
    directories = []
    for directory in os.listdir('./application'):
        if os.path.isfile(os.path.join('./application', directory, '__init__.py')) and \
        os.path.isfile(os.path.join('./application', directory, 'controllers', '__init__.py')) and \
        os.path.isdir(os.path.join('./application', directory, 'views')):
            directories.append(directory)
    directories = sort_names(directories)
    
    ###################################################################################################
    # get directory controller modules
    ###################################################################################################
    # directory_controller_modules is a dictionary with directory name as key 
    # and array of controller as value
    directory_controller_modules = {}
    for directory in directories:
        for file_name in os.listdir('./application/'+directory+'/controllers'):
            # get module inside directory's controller
            file_name_segments = file_name.split('.')
            first_segment = file_name_segments[0]
            last_segment = file_name_segments[-1]
            if (first_segment == '__init__') or (not last_segment == 'py'):
                continue
            module_name = inspect.getmodulename(file_name)
            if module_name is None:
                continue
            if not directory in directory_controller_modules:
                directory_controller_modules[directory] = []
            directory_controller_modules[directory].append(module_name)
    
    
    ###################################################################################################
    # Load everything inside controller modules
    ###################################################################################################
    for directory in directories:
        for controller_module in directory_controller_modules[directory]:
            # load everything inside the controllers
            print('LOAD CONTROLLER : '+controller_module)
            exec('from application.'+directory+'.controllers.'+controller_module+' import *')
                
    ###################################################################################################
    # Load Default_Controller inside controller modules
    ###################################################################################################
    for directory in directories:
        for controller_module in directory_controller_modules[directory]:
            module_obj = None
            exec('import application.'+directory+'.controllers.'+controller_module+' as module_obj')
            members = inspect.getmembers(module_obj, inspect.isclass)
            # determine if default_controller exists
            default_controller_found = False
            Default_Controller = None
            for member in members:
                if member[0] == 'Default_Controller':
                    default_controller_found = True
                    Default_Controller = member[1]
                    break
            # skip if there is no default_controller
            if not default_controller_found:
                continue
            # make an instance of Default_Controller
            controller = Default_Controller()            
            methods = inspect.getmembers(controller, inspect.ismethod)
            methods = sort_names(methods, 0)
            for method in methods:
                method_name = str(method[0])
                method_object = method[1]
                name_segments = method_name.split('_')
                # ignore functions without "action" prefix
                if not name_segments[0] == 'action':
                    continue 
                method_published_name = "_".join(name_segments[1:])
                parameters = inspect.getargspec(method_object)[0][1:]
                routes = get_routes(directory, controller_module, method_published_name, parameters)
                for route in routes:
                    app.route(route)(method_object)
    
            
    ###################################################################################################
    # serve application's static file
    ###################################################################################################
    print('ADD STATIC FILE ROUTE : /favicon.ico, /human.txt')
    print('ADD STATIC FILE ROUTE: "/images/*, /css/*, /js/*, /fonts/*')
    @app.route('/<path:re:(favicon.ico|humans.txt)>')
    @app.route('/<path:re:(static_libraries|images|css|js|fonts)\/.+>')
    def application_static(path):
        return static_file(path, root='application/static')
    
    ###################################################################################################
    # serve module's static file
    ###################################################################################################
    directory_pattern = '|'.join(directories)
    print('ADD STATIC FILE ROUTE: "module/static_libraries/*, module/images/*, module/css/*, module/js/*, module/fonts/*')
    @app.route('/<module_path:re:('+directory_pattern+')>/<path:re:(static_libraries|images|css|js|fonts)\/.+>')
    def module_static(module_path, path):
        return static_file(path, root='application/'+module_path+'/static')
    
    ###################################################################################################
    # add template path
    ###################################################################################################
    for directory in directories:
        print('REGISTER TEMPLATE PATH : '+directory+'/views/')
        TEMPLATE_PATH.append('./application/'+directory+'/views/')
    
    ###################################################################################################
    # run app with given parameters
    ###################################################################################################
    port = int(os.environ.get("PORT", PORT))
    run(app, reloader=RELOADER, host=HOST, port=port)