#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
# RUN THE SERVER
###########################################################################
def main_process(host, port, debug, reloader, server, app_directory):
    import os
    from kokoropy import kokoro_init
    PWD = os.path.dirname(os.path.abspath(__file__))
    application_path    = os.path.join(PWD, app_directory)
    kokoro_init(application_path = application_path, debug=debug,
                port=port, reloader=reloader, host=host, server=server)

if __name__ == '__main__':
    import sys, getopt
    args = sys.argv[1:]
    # pass arguments
    options, remainder = getopt.getopt(args, '', ['debug', 'reload', 'host=', 'port=', 'server=', 'appdir='])
    host = 'localhost'
    port = 8080 
    debug = True
    reloader = False
    server = 'kokoro'
    app_directory = 'applications'
    for opt, arg in options:
        if opt == 'debug':
            debug = True
        elif opt == 'reload':
            reloader = True
        elif opt == 'host':
            host = arg
        elif opt == 'port':
            port = arg
        elif opt == 'server':
            server = arg
        elif opt == 'appdir':
            app_directory = arg
    
    main_process(host, port, debug, reloader, server, app_directory)