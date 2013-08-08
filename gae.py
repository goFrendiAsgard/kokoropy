import os, sys
print __file__
'''
os.chdir(os.path.dirname(__file__))
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))
'''

import kokoropy

PWD = os.path.dirname(os.path.abspath(__file__))
APP_DIRECTORY = 'applications'
APPLICATION_PATH = os.path.join(PWD, APP_DIRECTORY)
kokoropy.set_runtime_path('.gae_runtime/')
kokoropy.set_base_url('/')
application = kokoropy.kokoro_init(server='gae', application_path = APPLICATION_PATH, run = False)
