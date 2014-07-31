'''
# Here you should define your routes, hooks and errors
# To define your routes, you can do this:
    from ..controllers.some_module import a_function
    def index:
        return 'hello world';
    def hello_world(name):
        return 'something else';
        
    urls = (
            ('/', index), 
            ('hello/<name>', hello_world),
            ('manage', a_function)
        )
    
# Aside from urls tuples, you can also use gets, posts, puts, and deletes tuple to achieve RESTful url
    posts = (('save', some_function),)
    
# To define hooks and errors, you can do this:
    hooks(
            ('before_request', some_function),
            ('after_request', some_function)
        )
    error(
            ('404', some_function),
            ('500', some_function)
        )
'''

urls  = ()
gets  = ()
posts = ()
puts  = ()
deletes = ()
hooks = ()
errors = ()