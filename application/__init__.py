# -*- coding: utf-8 -*-

#########################################################################
# APPLICATION PROGRAM (Please stay away from this)
#   Since kokoropy is open source, you are free to edit this
#   Just make sure you don't wake up the dragon.
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
#   (The same dragon who guard Laravel Realm)  .'  b .~~
#                                              :bb ,' 
#                                              ~~~~
#
# Still have a gut to edit this?
# Well, the warning has been given, your fate is now your own
#
#########################################################################

__version__ = '0.1'
from kokoropy.bottle import Bottle, TEMPLATE_PATH, static_file
import os, glob

#########################################################################
# get all kokoropy module directories
#########################################################################
directories = []
for directory in os.listdir('./application'):
    if os.path.isfile(os.path.join('./application', directory, '__init__.py')) and \
    os.path.isfile(os.path.join('./application', directory, 'controllers', '__init__.py')) and \
    os.path.isdir(os.path.join('./application', directory, 'views')):
        directories.append(directory)

app = Bottle()
TEMPLATE_PATH.remove('./views/')

#########################################################################
# add template path
#########################################################################
for directory in directories:    
    TEMPLATE_PATH.append('./application/'+directory+'/views/')
    print 'REGISTER TEMPLATE PATH : '+directory+'/views/'
    
#########################################################################
# load controllers
#########################################################################
for directory in directories:
    for file_name in os.listdir('./application/'+directory+'/controllers'):
        [file_name, extension] = file_name.split('.')
        if(extension == 'py' and not file_name == '__init__'):
            exec('from '+directory+'.controllers.'+file_name+' import *')
            print 'LOAD CONTROLLER : '+directory+'.controllers.'+file_name

#########################################################################
# serve application's static file
#########################################################################
@app.route('/<path:re:(favicon.ico|humans.txt)>')
@app.route('/<path:re:(images|css|js|fonts)\/.+>')
def application_static(path):
    return static_file(path, root='application/static')

#########################################################################
# serve kokoropy module's static file
#########################################################################
directory_pattern = '|'.join(directories)
@app.route('/<module_path:re:('+directory_pattern+')>/<path:re:(images|css|js|fonts)\/.+>')
def module_static(module_path, path):
    return static_file(path, root='application/'+module_path+'/static')