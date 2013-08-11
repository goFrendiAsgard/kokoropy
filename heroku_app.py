'''
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
import kokoropy

PWD = './'
if os.path.dirname(__file__) == '':
    PWD = os.getcwd()
else:
    PWD = os.path.dirname(__file__)
os.chdir(PWD)
if PWD not in sys.path:
    sys.path.append(PWD)

APP_DIRECTORY = 'applications'
APPLICATION_PATH = os.path.join(PWD, APP_DIRECTORY)
application = kokoropy.kokoro_init(server='gunicorn', port=os.environ.get('PORT', 5000),
                                   application_path = APPLICATION_PATH, run = False, 
                                   runtime_path = os.path.join(tempfile.gettempdir(), '.heroku_runtime/'), 
                                   base_url = '/')

if __name__ == '__main__':
    print "=== Run the server ==="
    kokoropy.run(app=application, server='gunicorn', port=os.environ.get('PORT', 5000))

