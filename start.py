#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# CONFIGURATION (Feel free to modify it)
###########################################################################
HOST                = 'localhost'
PORT                = 8080
DEBUG               = True
RELOADER            = False
SERVER              = 'kokoro' # or wsgiref or whatever
APP_DIRECTORY       = 'applications'

###########################################################################
# RUN THE SERVER
###########################################################################
def main_process():
    import os
    from kokoropy import kokoro_init
    PWD = os.path.dirname(os.path.abspath(__file__))
    APPLICATION_PATH    = os.path.join(PWD, APP_DIRECTORY)
    kokoro_init(application_path = APPLICATION_PATH, debug=DEBUG,
                port=PORT, reloader=RELOADER, host=HOST, server=SERVER)

if __name__ == '__main__':
    main_process()