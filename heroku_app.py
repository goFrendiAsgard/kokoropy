import os, tempfile
# import sys
# os.chdir(os.path.dirname(__file__))
# if os.path.dirname(__file__) not in sys.path:
#     sys.path.append(os.path.dirname(__file__))

import kokoropy

# PWD = os.path.dirname(os.path.abspath(__file__))
# APP_DIRECTORY = 'applications'
# APPLICATION_PATH = os.path.join(PWD, APP_DIRECTORY)

APPLICATION_PATH = './applications'
application = kokoropy.kokoro_init(server='gevent', port=os.environ.get('PORT', 5000),
                                   application_path = APPLICATION_PATH, run = True, 
                                   runtime_path = os.path.join(tempfile.gettempdir(), '.heroku_runtime/'), 
                                   base_url = '/')