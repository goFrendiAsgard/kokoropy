import os, tempfile
import kokoropy

kokoropy.kokoro_init(server='gevent', port=os.environ.get('PORT', 5000), application_path = './applications', run = True, runtime_path = os.path.join(tempfile.gettempdir(), '.heroku_runtime/'), base_url = '/')