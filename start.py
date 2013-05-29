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
# DON'T TOUCH FOLLOWING CODES
###########################################################################
import os, subprocess, signal, time

def start_server():
    PWD = os.path.dirname(os.path.abspath(__file__))
    SCRIPT_PATH = os.path.join(PWD,'bootstrapper.py')
    RUN_COMMAND = '%s --host=%s --port=%d --server=%s --appdir=%s' %(SCRIPT_PATH, HOST, PORT, SERVER, APP_DIRECTORY)
    if RELOADER:
        RUN_COMMAND += ' --reload'
    if DEBUG:
        RUN_COMMAND += ' --debug'
    return subprocess.Popen(SCRIPT_PATH)


if __name__ == '__main__':
    STOP_FLAG = False
    while not STOP_FLAG:
        try:
            PROCESS = start_server()
            time.sleep(10)
            os.kill(PROCESS.pid, signal.SIGINT)
        except(KeyboardInterrupt, SystemExit):
            STOP_FLAG = True
    print ("Kokoropy Server Ended")