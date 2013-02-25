# -*- coding: utf-8 -*-

#########################################################################
#
# MAIN KOKOROPY PROGRAM
# * This will load all of your controllers and views
# * Normally there is no need to edit this file
#
#########################################################################

__version__ = '0.1'
from kokoropy.bottle import Bottle, TEMPLATE_PATH, static_file
import os

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