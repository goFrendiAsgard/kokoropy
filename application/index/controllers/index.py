from kokoropy.bottle import route, request

# modify this file as you want

@route('/')
def index():
    if 'counter' in request.session:
        request.session['counter'] += 1
    else:
        request.session['counter'] = 1
    return '''
        <title>Kokoropy</title>
        <h1>It works</h1>
        <h3>You have visit this page '''+str(request.session['counter'])+''' times</h3>
        <a href="/example/recommended">Check the example</a>'''