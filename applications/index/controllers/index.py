from kokoropy import route, request

# modify this file as you want

@route('/')
def index():    
    # return string
    response  = '<title>Kokoropy</title>'
    response += '<h1>It works !!!</h1>'
    response += '<a href="'+request.BASE_URL+'example/recommended">Check the example</a>'
    return response