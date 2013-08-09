#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# CONFIGURATION (Feel free to modify it)
###########################################################################
HOST                = 'localhost'               # the server name
PORT                = 8080                      # http port
DEBUG               = True                      # True or False
RELOADER            = False                     # True or False
SERVER              = 'kokoro'                  # or wsgiref or whatever
APP_DIRECTORY       = 'applications'            # applications package
RUNTIME_PATH        = '.development_runtime'    # runtime path
BASE_URL            = '/kokoropy'                       # base url, start with '/'

###########################################################################
# DON'T TOUCH FOLLOWING CODES
###########################################################################
import sys, os, subprocess, signal, time, datetime

FILE_STAT = {}

def start_server():
    PWD = os.path.dirname(os.path.abspath(__file__))
    SCRIPT_PATH = os.path.join(PWD,'bootstrapper.py')
    RUN_COMMAND = '%s %s' %(sys.executable, SCRIPT_PATH)
    ARGUMENTS = '--host=%s --port=%d --server=%s --appdir=%s --baseurl=%s --runtimepath=%s' %(HOST, PORT, SERVER, APP_DIRECTORY, BASE_URL, RUNTIME_PATH)
    if RELOADER:
        ARGUMENTS += ' --reload'
    if DEBUG:
        ARGUMENTS += ' --debug'
    RUN_COMMAND = RUN_COMMAND + ' ' + ARGUMENTS
    return subprocess.Popen(RUN_COMMAND, shell=True, preexec_fn=os.setsid)

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def is_modified():
    MODIFICATION_FLAG = False
    PWD = os.path.dirname(os.path.abspath(__file__))
    APP_PATH = os.path.join(PWD, APP_DIRECTORY)
    CHECKED_STAT = []
    REMOVED_STAT = []
    for dirpath, dirnames, filenames in os.walk(APP_PATH, topdown=True):
        del dirnames
        for filename in filenames:
            absolute_filename = os.path.join(dirpath, filename)
            last_change = modification_date(absolute_filename)
            if (absolute_filename not in FILE_STAT) or (FILE_STAT[absolute_filename] != last_change):
                FILE_STAT[absolute_filename] = last_change
                MODIFICATION_FLAG = True
            CHECKED_STAT.append(absolute_filename)
    # check if there are deleted file
    for absolute_filename in FILE_STAT:
        if absolute_filename not in CHECKED_STAT:
            REMOVED_STAT.append(absolute_filename)
            MODIFICATION_FLAG = True
    # delete it from FILE_STAT
    for absolute_filename in REMOVED_STAT:
        FILE_STAT.pop(absolute_filename,None)
    return MODIFICATION_FLAG


if __name__ == '__main__':
    STOP_FLAG = False
    PROCESS = None
    print ('KOKOROPY DEBUGGING SESSION\n')
    while not STOP_FLAG:
        try:
            MODIFIED = is_modified()
            if MODIFIED:
                if PROCESS is not None:
                    os.killpg(PROCESS.pid, signal.SIGTERM)
                PROCESS = start_server()
            time.sleep(1)
        except(KeyboardInterrupt, SystemExit):
            STOP_FLAG = True
    if PROCESS is not None:
        os.killpg(PROCESS.pid, signal.SIGTERM)
    print ("\nEND OF KOKOROPY DEBUGGING SESSION")