import os, tempfile
from kokoropy import bottle

 
@bottle.route("/")
def index():
    return "Hello World"
 
bottle.run(server="gevent", port=os.environ.get("PORT", 5000))
#kokoropy.kokoro_init( server='gevent', port=os.environ.get('PORT', 5000), application_path = './applications', run = True, runtime_path = os.path.join(tempfile.gettempdir(), '.heroku_runtime/'), base_url = '/')