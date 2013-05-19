import os, sys
os.chdir(os.path.dirname(__file__))
sys.path = [os.path.dirname(__file__)] + sys.path

from kokoropy import kokoro_init

PWD = os.path.dirname(os.path.abspath(__file__))
APP_DIRECTORY = 'applications'
APPLICATION_PATH = os.path.join(PWD, APP_DIRECTORY)    
application = kokoro_init(application_path = APPLICATION_PATH, run = False)