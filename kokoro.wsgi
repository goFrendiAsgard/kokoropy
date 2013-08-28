import os, sys, tempfile
os.chdir(os.path.dirname(__file__))
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

import kokoropy

PWD = os.path.dirname(os.path.abspath(__file__))
APP_DIRECTORY = 'applications'
APPLICATION_PATH = os.path.join(PWD, APP_DIRECTORY)
application = kokoropy.kokoro_init(application_path = APPLICATION_PATH, run = False, 
                                   runtime_path = os.path.join(tempfile.gettempdir(), '.apache_runtime/'), 
                                   base_url = '/')