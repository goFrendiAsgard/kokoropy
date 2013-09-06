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
                                   runtime_path = '.heroku_runtime/', 
                                   base_url = '/')

if __name__ == '__main__':
    print "=== Run the server ==="
    kokoropy.run(app=application, server='gunicorn', host='0.0.0.0', port=os.environ.get('PORT', 5000), workers=3)
