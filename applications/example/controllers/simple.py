from kokoropy import route, base_url

"""
Simple routing (without OOP)
This is great to make a "hello world" or other small applications
"""
@route(base_url('example/simple/hello_world'))
def index():
    html_response  = 'This is just a very simple hello world !!!<br />'
    html_response += '<a href="'+base_url('/example/recommended')+'">See cooler things here</a>'
    return html_response