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
RUNTIME_PATH        = '.development_runtime'    # runtime path
BASE_URL            = '/kokoropy'               # base url, start with '/'

###########################################################################
# DON'T TOUCH FOLLOWING CODES
###########################################################################
import subprocess, signal, time, datetime, os, sys, getopt, kokoropy
from kokoropy import Fore, Back

VERSION   = '0.0.1'
PWD       = os.path.dirname(os.path.abspath(__file__))
FILE_STAT = {}

#####################################################################################################
# RUN THE SERVER
#####################################################################################################
def _run_server(host, port, debug, reloader, server, base_url, runtime_path):
    kokoropy.kokoro_init(debug=debug, port=port, reloader=reloader,
                         host=host, server=server, base_url=base_url, runtime_path=runtime_path)

def run_server_once():
    
    args = sys.argv[2:]
    # pass arguments
    options, remainder = getopt.getopt(args, '', ['debug', 'reload', 'host=', 'port=', 'server=', 
                                                  'baseurl=', 'runtimepath='])
    host = 'localhost'
    port = 8080 
    debug = True
    reloader = False
    server = 'kokoro'
    app_directory = 'applications'
    runtime_path = '.runtime/'
    base_url = '/'
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
        elif opt == 'runtimepath':
            runtime_path = arg
        elif opt == 'baseurl':
            base_url = arg
                
    _run_server(host, port, debug, reloader, server, base_url, runtime_path)

def _run_server_as_subprocess():
    SCRIPT_PATH = os.path.abspath(__file__)
    RUN_COMMAND = '%s %s' %(sys.executable, SCRIPT_PATH)
    ARGUMENTS = 'run_server_once --host=%s --port=%d --server=%s --baseurl=%s --runtimepath=%s' %(HOST, PORT, SERVER, BASE_URL, RUNTIME_PATH)
    if RELOADER:
        ARGUMENTS += ' --reload'
    if DEBUG:
        ARGUMENTS += ' --debug'
    RUN_COMMAND = RUN_COMMAND + ' ' + ARGUMENTS
    return subprocess.Popen(RUN_COMMAND, shell=True)

def _get_modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def _is_anything_modified():
    MODIFICATION_FLAG = False
    CHECKED_STAT = []
    REMOVED_STAT = []
    exclude = ('assets', 'db', 'migrations')
    
    for dirpath, dirnames, filenames in os.walk('./applications', topdown=True):
        del dirnames
        dirpart = dirpath.split('/')
        if len(dirpart)>3 and dirpart[3] in exclude:
            continue
        for filename in filenames:
            absolute_filename = os.path.join(dirpath, filename)
            last_change = _get_modification_date(absolute_filename)
            # check if there are some added or edited files
            if (absolute_filename not in FILE_STAT) or (FILE_STAT[absolute_filename] != last_change):
                FILE_STAT[absolute_filename] = last_change
                MODIFICATION_FLAG = True
            CHECKED_STAT.append(absolute_filename)
    # check if there are some deleted files
    for absolute_filename in FILE_STAT:
        if absolute_filename not in CHECKED_STAT:
            REMOVED_STAT.append(absolute_filename)
            MODIFICATION_FLAG = True
    # delete it from FILE_STAT
    for absolute_filename in REMOVED_STAT:
        FILE_STAT.pop(absolute_filename,None)
    return MODIFICATION_FLAG

def run_server_forever():
    STOP_FLAG = False
    PROCESS = None
    print ('%sDevelopment Server Started ...%s\n' % (Fore.MAGENTA, Fore.RESET))
    while not STOP_FLAG:
        try:
            MODIFIED = _is_anything_modified()
            if MODIFIED:
                if PROCESS is not None:
                    os.kill(PROCESS.pid, signal.SIGTERM)
                PROCESS = _run_server_as_subprocess()
            time.sleep(1)
        except(KeyboardInterrupt, SystemExit):
            STOP_FLAG = True
    if PROCESS is not None:
        os.kill(PROCESS.pid, signal.SIGTERM)
    print ('\n%sDevelopment Server Stopped ...%s\n' % (Fore.MAGENTA, Fore.RESET))

def scaffold_application():
    if len(sys.argv)>2:
        application_name = sys.argv[2]
        kokoropy.scaffold_application(application_name)
    else:
        help()

def scaffold_migration():
    if len(sys.argv)>3:
        application_name = sys.argv[2]
        migration_name = sys.argv[3]
        if len(sys.argv)>4:
            table_name = sys.argv[4]
        else:
            table_name = 'table'
        if len(sys.argv)>5:
            columns = sys.argv[5:]
        else:
            columns = []
        kokoropy.scaffold_migration(application_name, migration_name, table_name, *columns)
    else:
        help()

def scaffold_model():
    if len(sys.argv)>3:
        application_name = sys.argv[2]
        if len(sys.argv)>3:
            table_name = sys.argv[3]
        else:
            table_name = 'table'
        if len(sys.argv)>4:
            columns = sys.argv[4:]
        else:
            columns = []
        kokoropy.scaffold_model(application_name, table_name, *columns)
    else:
        help()

def scaffold_crud():
    if len(sys.argv)>3:
        application_name = sys.argv[2]
        if len(sys.argv)>3:
            table_name = sys.argv[3]
        else:
            table_name = 'table'
        if len(sys.argv)>4:
            columns = sys.argv[4:]
        else:
            columns = []
        kokoropy.scaffold_crud(application_name, table_name, *columns)
    else:
        help()
        
def migration_upgrade():
    if len(sys.argv)>2:
        application_name = sys.argv[2]
        kokoropy.migration_upgrade(application_name)
    else:
        kokoropy.migration_upgrade()

def migration_downgrade():
    if len(sys.argv)>2:
        application_name = sys.argv[2]
        kokoropy.migration_downgrade(application_name)

def migration_log():
    migrations = {}
    if len(sys.argv)>2:
        application_name = sys.argv[2]
        migrations[application_name] = kokoropy.migration_log(application_name)
    else:
        migrations = kokoropy.migration_log()
    for key in migrations:
        print (' * APPLICATION NAME : %s ' % key)
        for migration in migrations[key]:
            print ('     %s' % migration.migration_name)

def info():
    print('')
    print(' %sVERSION:%s %s\n' % (Fore.MAGENTA, Fore.RESET, VERSION))
    print(' %sUSAGE:%s\n' % (Fore.MAGENTA, Fore.RESET))
    print(' * Help')
    print('     %spython %s%s help%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.RESET))
    print(' * Run Server')
    print('     %spython %s%s start%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.RESET))
    print(' * Scaffold Application')
    print('     %spython %s%s scaffold-application %sAPPLICATION-NAME%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.BLUE, Fore.RESET))
    print(' * Scaffold Migration')
    print('     %spython %s%s scaffold-migration %sAPPLICATION-NAME MIGRATION-NAME [table-name] [column-name:type] ... %s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.BLUE, Fore.RESET))
    print(' * Scaffold Model')
    print('     %spython %s%s scaffold-model %sAPPLICATION-NAME [table-name] [column-name:type] ... %s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.BLUE, Fore.RESET))
    print(' * Scaffold CRUD')
    print('     %spython %s%s scaffold-crud %sAPPLICATION-NAME [table-name] [column-name:type] ... %s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.BLUE, Fore.RESET))
    print(' * Migration upgrade (to the newest version)')
    print('     %spython %s%s migration-upgrade %s[APPLICATION-NAME]%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.BLUE, Fore.RESET))
    print(' * Migration downgrade (to the previous version)')
    print('     %spython %s%s migration-downgrade %sAPPLICATION-NAME%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.BLUE, Fore.RESET))
    print(' * List of migration applied')
    print('     %spython %s%s migration-log %s[APPLICATION-NAME]%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.BLUE, Fore.RESET))

if __name__ == '__main__':
    # define function_dict
    function_dict = {
            'run_server_once' : run_server_once,
            'start' : run_server_forever,
            'scaffold-application' : scaffold_application,
            'scaffold-migration' : scaffold_migration,
            'scaffold-model' : scaffold_model,
            'scaffold-crud' : scaffold_crud,
            'migration-upgrade' : migration_upgrade,
            'migration-downgrade' : migration_downgrade,
            'migration-log' : migration_log,
            'help' : info
        }
    # get action
    action = sys.argv[1] if len(sys.argv)>1 else 'help'
    if action not in function_dict:
        action = 'help'
    # execute the action
    function_dict[action]()