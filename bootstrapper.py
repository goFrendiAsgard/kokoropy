#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys, getopt
    args = sys.argv[1:]
    # pass arguments
    options, remainder = getopt.getopt(args, '', ['debug', 'reload', 'host=', 'port=', 'server=', 'appdir=', 'baseurl=', 'runtimepath='])
    host = 'localhost'
    port = 8080 
    debug = True
    reloader = False
    server = 'kokoro'
    app_directory = 'applications'
    runtime_path = '.runtime/'
    for opt, arg in options:
        if opt[0:2] == '--':
            opt = opt[2:]
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
        elif opt == 'runtimepath':
            runtime_path = arg
            
    ###########################################################################
    # RUN THE SERVER (Why put it here? because we need BASE_URL & RUNTIME_PATH)
    ###########################################################################
    def main_process(host, port, debug, reloader, server, app_directory):
        import os
        import kokoropy
        PWD = os.path.dirname(os.path.abspath(__file__))
        application_path      = os.path.join(PWD, app_directory)
        kokoropy.runtime_path(runtime_path)
        kokoropy.kokoro_init(application_path = application_path, debug=debug,
                    port=port, reloader=reloader, host=host, server=server)          
                
    main_process(host, port, debug, reloader, server, app_directory)