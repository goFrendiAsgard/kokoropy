from kokoropy import route

"""
Simple routing (without OOP)
This is great to make a "hello world" or other small applications
"""

@route('/example/simple/hello_world')
def index():
    return '''This is a very simple hello world !!!<br />
        <a href="/example/recommended">Now go back to work</a>'''