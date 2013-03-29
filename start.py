#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################################################
# import "standard" modules (Please leave it as is)
########################################################################################################
import inspect
from kokoropy import kokoro_init, template
custom_404, custom_403, custom_500 = None, None, None

########################################################################################################
# CONFIGURATION (Feel free to modify it)
########################################################################################################
HOST                = 'localhost'
PORT                = 8080
DEBUG               = True
RELOADER            = True
SERVER              = 'wsgiref'

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


if __name__ == '__main__':
    
    if inspect.isfunction(custom_404) and inspect.isfunction(custom_403) and inspect.isfunction(custom_500):
        ERROR_HANDLER = {
            404 : custom_404,
            403 : custom_403,
            500 : custom_500
        }
    else:
        ERROR_HANDLER = {}
    
    ###################################################################################################
    # run app with given parameters
    ###################################################################################################
    kokoro_init(debug=DEBUG, port=PORT, reloader=RELOADER, host=HOST, error_handler=ERROR_HANDLER, server=SERVER)    