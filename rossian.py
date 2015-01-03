#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, signal, time, datetime, os, sys, getopt, kokoropy

from kokoropy import Fore, Back, scaffold

VERSION   = '0.0.1'
PWD       = os.path.dirname(os.path.abspath(__file__))
FILE_STAT = {}

#####################################################################################################
# RUN THE SERVER
#####################################################################################################

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
    kokoropy.kokoro_init(debug=debug, port=port, reloader=reloader,
                         host=host, server=server, base_url=base_url, runtime_path=runtime_path)

def _run_server_as_subprocess():
    args = sys.argv[2:]
    # pass arguments
    options, remainder = getopt.getopt(args, '', ['debug', 'reload', 'host=', 'port=', 'server=', 
                                                  'baseurl=', 'runtimepath='])
    host = 'localhost'
    port = 8080 
    debug = True
    reloader = False
    server = 'kokoro'
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
    SCRIPT_PATH = os.path.abspath(__file__)
    RUN_COMMAND = '%s %s' %(sys.executable, SCRIPT_PATH)
    ARGUMENTS = 'run_server_once --host=%s --port=%d --server=%s --baseurl=%s --runtimepath=%s' %(host, port, server, base_url, runtime_path)
    if reloader:
        ARGUMENTS += ' --reload'
    if debug:
        ARGUMENTS += ' --debug'
    RUN_COMMAND = RUN_COMMAND + ' ' + ARGUMENTS
    if hasattr(os, 'setsid'):
        return subprocess.Popen(RUN_COMMAND, shell=True, preexec_fn=os.setsid)
    else:
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
            if not os.path.exists(absolute_filename):
                continue
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

def _kill_process(process):
    if process is not None:
        if hasattr(os, 'killpg'):
            os.killpg(process.pid, signal.SIGTERM)
        else:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])

def run_server_forever():
    print ('%sDevelopment Server Started ...%s\n' % (Fore.MAGENTA, Fore.RESET))
    STOP_FLAG = False
    PROCESS = None
    try:
        while not STOP_FLAG:
            try:
                MODIFIED = _is_anything_modified()
                if MODIFIED:
                    _kill_process(PROCESS)
                    PROCESS = _run_server_as_subprocess()
                time.sleep(1)
            except(KeyboardInterrupt, SystemExit):
                STOP_FLAG = True
    finally:
        _kill_process(PROCESS)
    print ('\n%sDevelopment Server Stopped ...%s\n' % (Fore.MAGENTA, Fore.RESET))

def _do_thing(fn, min_param = 0, success_message = ''):
    if len(sys.argv) == 3 and min_param > 1:
        file_name = sys.argv[2]
        if os.path.isfile(file_name):
            # read content of file as 1 line
            content = ' '.join(open(file_name, 'r').readlines())
            # remove multiple spaces
            content = ' '.join(content.split())
            # split it again
            args = content.split(' ')
        else:
            print (Fore.RED + ' * ERROR: File \''+ file_name +'\' not found' + Fore.RESET)
            return False
    elif len(sys.argv) >= 2 + min_param:
        args = sys.argv[2 :]
    else:
        info()
        return False
    fn(*args)
    if success_message != '':
        print (Fore.MAGENTA + ' * ' +success_message + Fore.RESET)

def scaffold_application():
    _do_thing(scaffold.scaffold_application, 1, 'Application Created')

def scaffold_migration():
    _do_thing(scaffold.scaffold_migration, 3, 'Migration Created')

def scaffold_model():
    _do_thing(scaffold.scaffold_migration, 3, 'Model Created')

def scaffold_crud():
    _do_thing(scaffold.scaffold_crud, 3, 'CRUD Created')

def scaffold_view():
    _do_thing(scaffold.scaffold_view, 1, 'View Created')

def scaffold_cms():
    _do_thing(scaffold.scaffold_cms, 0, 'CMS Created')
        
def migration_upgrade():
    if len(sys.argv)>2:
        application_name = sys.argv[2]
        kokoropy.migration_upgrade(application_name)
    else:
        kokoropy.migration_upgrade()
    print(' * Upgrade Complete')

def migration_downgrade():
    if len(sys.argv)>2:
        application_name = sys.argv[2]
        kokoropy.migration_downgrade(application_name)
    print(' * Downgrade Complete')

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
    print(' %s VERSION: %s %s\n' % (Fore.WHITE + Back.RED, Back.RESET + Fore.RESET, VERSION))
    print(' %s USAGE: %s\n' % (Fore.WHITE + Back.RED, Back.RESET + Fore.RESET))
    print(' * Help')
    print('     %spython %s%s help%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.RESET))
    print(' * Run Server')
    print('     %spython %s%s start %s[--host=localhost --port=8080 --server=kokoro --baseurl=/ --runtimepath=.runtime --debug --reload]%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * Scaffold Application')
    print('     %spython %s%s scaffold-application %sAPPLICATION-NAME%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * Scaffold Migration')
    print('     %spython %s%s scaffold-migration %sAPPLICATION-NAME MIGRATION-NAME table-name [column-name:type] ... %s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * Scaffold Model')
    print('     %spython %s%s scaffold-model %sAPPLICATION-NAME table-name [column-name:type] ... %s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * Scaffold CRUD')
    print('     %spython %s%s scaffold-crud %sAPPLICATION-NAME table-name [column-name:type] ... %s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * Scaffold View (to make custom CRUD view)')
    print('     %spython %s%s scaffold-view %sAPPLICATION-NAME table-name [view]%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * Scaffold CMS')
    print('     %spython %s%s scaffold-cms %s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.RESET))
    print(' * Migration upgrade (to the newest version)')
    print('     %spython %s%s migration-upgrade %s[APPLICATION-NAME]%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * Migration downgrade (to the previous version)')
    print('     %spython %s%s migration-downgrade %sAPPLICATION-NAME%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))
    print(' * List of migration applied')
    print('     %spython %s%s migration-log %s[APPLICATION-NAME]%s\n' % (Fore.GREEN, __file__, Fore.YELLOW, Fore.MAGENTA, Fore.RESET))

if __name__ == '__main__':
    # define function_dict
    function_dict = {
            'run_server_once' : run_server_once,
            'start' : run_server_forever,
            'scaffold-application' : scaffold_application,
            'scaffold-migration' : scaffold_migration,
            'scaffold-model' : scaffold_model,
            'scaffold-crud' : scaffold_crud,
            'scaffold-view' : scaffold_view,
            'scaffold-cms'  : scaffold_cms,
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
