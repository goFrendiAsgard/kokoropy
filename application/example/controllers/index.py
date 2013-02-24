from application import app

@app.route('/', method='GET')
def index():
    return "Hello world"