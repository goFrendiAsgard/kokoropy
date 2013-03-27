from kokoropy.bottle import route

## SIMPLE APPROACH (Simple but deadly works) #############################################
#
# A very simple procedural style example
# Manually routed to http://localhost:8080/example/simple with @route decorator
##########################################################################################

@route('/example/simple/hello_world')
def index():
    return '''This is a very simple hello world !!!<br />
        <a href="/example/recommended">Now go back to work</a>'''