import os, sys, tempfile

PWD = './'
if os.path.dirname(__file__) == '':
    PWD = os.getcwd()
else:
    PWD = os.path.dirname(__file__)
os.chdir(PWD)
if PWD not in sys.path:
    sys.path.append(PWD)

import kokoropy

APP_DIRECTORY = 'applications'
APPLICATION_PATH = os.path.join(PWD, APP_DIRECTORY)
application = kokoropy.kokoro_init(port=os.environ.get('PORT', 5000),
                                   application_path = APPLICATION_PATH, run = True, 
                                   runtime_path = os.path.join(tempfile.gettempdir(), '.heroku_runtime/'), 
                                   base_url = '/')