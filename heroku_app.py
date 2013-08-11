import os, tempfile

from kokoropy.bottle import route, run

@route("/")
def hello_world():
        return "Hello World!"

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#kokoropy.kokoro_init( server='gevent', port=os.environ.get('PORT', 5000), application_path = './applications', run = True, runtime_path = os.path.join(tempfile.gettempdir(), '.heroku_runtime/'), base_url = '/')