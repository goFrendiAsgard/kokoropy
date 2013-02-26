#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################################################
# CONFIGURATION (Feel free to modify it)
########################################################################################################
HOST                = 'localhost'
PORT                = 8080
DEBUG               = True
RELOADER            = False



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
#   (This dragon also guards "laravel" realms)  .'  b .~~
#   (Make sure you know what you do)           :bb ,' 
#                                              ~~~~
#
########################################################################################################
#import os, sys
#lib_path = os.path.abspath('..')
#sys.path.append(lib_path)

import os, inspect

# import modules
from application import app
from kokoropy.bottle import debug, run, static_file, TEMPLATE_PATH

def sort_names(names=[], key=None):
    index_exists = False
    index_obj = None
    empty_exists = False
    empty_obj = None
    # remove some special element
    if not key is None:
        for i in xrange(len(names)):
            if names[i][key] == 'index':
                index_obj = names[i][key]
                index_exists = True
                names.remove(i)
            if names[i][key] == '':
                empty_obj = names[i][key]
                empty_exists = True
                names.remove(i)
            if index_exists and empty_exists:
                break
    else:
        if 'index' in names:
            index_obj = 'index'
            index_exists = True
            names.remove('index')            
        if '' in names:
            empty_obj = ''
            empty_exists = True
            names.remove('')        
    #sort the other normal elements
    names.sort(key = len, reverse=True)    
    # re add those removed special element
    if index_exists:
        names.append(index_obj)
    if empty_exists:
        names.appenc(empty_obj)    
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
            routes.append(basic_route+'/'+parameter_segment+'/<re:.*>')
        routes.append(basic_route)
        routes.append(basic_route+'/')
        routes.append(basic_route+'/<re:.*>')
    # return routes
    print routes
    return routes    


if __name__ == '__main__':
    # set debug mode
    debug(DEBUG)
    
    TEMPLATE_PATH.remove('./views/')
    
    # init directories
    print 'INIT APPLICATION DIRECTORIES'   
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
    # add template path
    ###################################################################################################
    for directory in directories:
        print 'REGISTER TEMPLATE PATH : '+directory+'/views/'
        TEMPLATE_PATH.append('./application/'+directory+'/views/')
        
    
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
    # Load everything inside controller modules (This will override default controller behaviour)
    ###################################################################################################
    for directory in directories:
        for controller_module in directory_controller_modules[directory]:
            # load everything inside the controllers
            print 'LOAD CONTROLLER : '+controller_module
            exec('from application.'+directory+'.controllers.'+controller_module+' import *')
        
    
    ###################################################################################################
    # serve application's static file
    ###################################################################################################
    print 'ADD STATIC FILE ROUTE : /favicon.ico, /human.txt'
    print 'ADD STATIC FILE ROUTE: "/images/*, /css/*, /js/*, /fonts/*'
    @app.route('/<path:re:(favicon.ico|humans.txt)>')
    @app.route('/<path:re:(images|css|js|fonts)\/.+>')
    def application_static(path):
        return static_file(path, root='application/static')
    
    ###################################################################################################
    # serve kokoropy module's static file
    ###################################################################################################
    directory_pattern = '|'.join(directories)
    print 'ADD STATIC FILE ROUTE: "module/images/*, module/css/*, module/js/*, module/fonts/*'
    @app.route('/<module_path:re:('+directory_pattern+')>/<path:re:(images|css|js|fonts)\/.+>')
    def module_static(module_path, path):
        return static_file(path, root='application/'+module_path+'/static')
    
    ###################################################################################################
    # run app with given parameters
    ###################################################################################################
    port = int(os.environ.get("PORT", PORT))
    run(app, reloader=RELOADER, host=HOST, port=port)