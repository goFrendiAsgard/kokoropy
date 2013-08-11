import os
from kokoropy.bottle import route, run

@route('/')
def index(name='World'):
    return 'Simple example'


if __name__ == '__main__':
    # Get required port, default to 5000.
    port = os.environ.get('PORT', 5000)

    # Run the app.
    run(host='0.0.0.0', port=port)
'''
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
'''