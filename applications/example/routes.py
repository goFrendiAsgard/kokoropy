from kokoropy import route, base_url, request, template, load_controller, load_view

"""
Simple routing (without OOP)
This is great to make a "hello world" or other small applications
"""
@route(base_url('example/simple/hello_world'))
def index():
    if 'counter' in request.SESSION:
        request.SESSION['counter'] += 1
    else:
        request.SESSION['counter'] = 1        
    # get say_hello
    message  = 'The session said that you have visit routing demo page '+str(request.SESSION['counter'])+' times'
    return load_view("example", "simple_hello", message=message)

# make a My_Controller instance and define the manual routing
My_Controller = load_controller('example', 'my_controller')
my_controller = My_Controller()
route(base_url("/example/advance/hello"))(my_controller.hello)
route(base_url("/example/advance/hello/"))(my_controller.hello)
route(base_url("/example/advance/hello/<name>"))(my_controller.hello)
route(base_url("/example/advance/hello/<name>/"))(my_controller.hello)