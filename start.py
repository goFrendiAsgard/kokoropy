#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# CONFIGURATION (Feel free to modify it)
#########################################################################
HOST                = 'localhost'
PORT                = 8080
DEBUG               = True
RELOADER            = True



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
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

# import modules
from application import app
from kokoropy.bottle import debug, run

# run kokoropy with given parameters
debug(DEBUG)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", PORT))
    run(app, reloader=RELOADER, host=HOST, port=port)