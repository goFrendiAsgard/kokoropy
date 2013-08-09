from kokoropy import route, base_url

# modify this file as you want

@route('/')
def index():    
    # return string
    html_response  = '<title>Kokoropy</title>'
    html_response += '<h1>It works !!!</h1>'
    html_response += '<a href="'+base_url('example/recommended')+'">Check the example</a>'
    return html_response