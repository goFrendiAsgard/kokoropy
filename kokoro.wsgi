import os, sys
import kokoropy

PWD = './'
if os.path.dirname(__file__) == '':
    PWD = os.path.abspath(os.getcwd())
else:
    PWD = os.path.dirname(os.path.abspath(__file__))
os.chdir(PWD)
if PWD not in sys.path:
    sys.path.append(PWD)

APP_DIRECTORY = 'applications'
APPLICATION_PATH = os.path.join(PWD, APP_DIRECTORY)
application = kokoropy.kokoro_init(application_path = APPLICATION_PATH, run = False, 
                                   runtime_path = '.apache_runtime/', 
                                   base_url = '/')