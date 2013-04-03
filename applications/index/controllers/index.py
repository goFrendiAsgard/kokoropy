from kokoropy import route, request

# modify this file as you want

@route('/')
def index():    
    # return string
    return '''
        <title>Kokoropy</title>
        <h1>It works</h1>
        <a href="/example/recommended">Check the example</a>'''