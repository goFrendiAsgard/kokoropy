#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# CONFIGURATION (Feel free to modify it)
#########################################################################
HOST                = 'localhost'
PORT                = 8080
DEBUG               = True
RELOADER            = False



#########################################################################
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
#########################################################################
#import os, sys
#lib_path = os.path.abspath('..')
#sys.path.append(lib_path)

import os

# import modules
from application import app, init_directories
from kokoropy.bottle import debug, run, static_file


if __name__ == '__main__':
    # set debug mode
    debug(DEBUG)
    
    # init directories
    print 'INIT APPLICATION DIRECTORIES'   
    directories = init_directories()    
    
    # serve application's static file
    print 'ADD STATIC FILE ROUTE : /favicon.ico, /human.txt'
    print 'ADD STATIC FILE ROUTE: "/images/*, /css/*, /js/*, /fonts/*'
    @app.route('/<path:re:(favicon.ico|humans.txt)>')
    @app.route('/<path:re:(images|css|js|fonts)\/.+>')
    def application_static(path):
        return static_file(path, root='application/static')
    
    # serve kokoropy module's static file
    directory_pattern = '|'.join(directories)
    print 'ADD STATIC FILE ROUTE: "module/images/*, module/css/*, module/js/*, module/fonts/*'
    @app.route('/<module_path:re:('+directory_pattern+')>/<path:re:(images|css|js|fonts)\/.+>')
    def module_static(module_path, path):
        return static_file(path, root='application/'+module_path+'/static')
    
    # run kokoropy with given parameters    
    port = int(os.environ.get("PORT", PORT))
    run(app, reloader=RELOADER, host=HOST, port=port)