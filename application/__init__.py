# -*- coding: utf-8 -*-

#########################################################################
#
# MAIN KOKOROPY PROGRAM
# * This will load all of your controllers and views
# * Normally there is no need to edit this file
#
#########################################################################

__version__ = '0.1'
from kokoropy.bottle import Bottle, error, template
import os

#########################################################################
# initialize bottle
#########################################################################
app = Bottle()

def custom_404(error):
    import random
    error_messages = [
        'Sorry, but there is no gray elephant in Atlantic ..',
        'You might be sure that the page should be here, in this case you are wrong',
        'Has you type the correctly write the URL?',
        'Go home you are drunk !!!',
    ]
    message_index = random.randrange(0,len(error_messages))
    error_message = error_messages[message_index]
    data = {
       'error_title'  : '404, Page not found',
       'error_message' : error_message
    }
    return template('example/error', data = data)

error_handler = {
    404 : custom_404,
}