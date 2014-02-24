#########################################################################################################
# Configuration name   : FIRST_TIME
# Default value        : True
# Alternative value    : True, False
# If you have modify something, and want to disable kokoropy's default home page, just set this to False
#########################################################################################################
FIRST_TIME = True

#########################################################################################################
# Configuration name   : CUSTOM_ERROR
# Default value        : False
# Alternative value    : True, False
# If you want to enable custom error, end let your visitor see the sarcastic-human word instead of
# any informative-for-developer info such as "404 Not found", set this to true
#########################################################################################################
CUSTOM_ERROR = False

#########################################################################################################
# End of configuration
#########################################################################################################

from kokoropy import route, load_view, base_url, template, remove_trailing_slash, error, hook

if FIRST_TIME:
    @route('/')
    @route(remove_trailing_slash(base_url()))
    @route(base_url())
    def index():    
        # return string
        return load_view('index', 'index.tpl', active_page = 'home')
    
    @route(remove_trailing_slash(base_url('getting_started')))
    @route(base_url('getting_started'))
    def index():    
        # return string
        return load_view('index', 'getting_started.tpl', active_page = 'getting_started')

if CUSTOM_ERROR:
    @hook('before_request')
    def _before_request():
        pass
    
    @hook('after_request')
    def _after_request():
        pass
    
    @error(404)
    def _error_404(error):
        import random
        error_messages = [
            'Sorry, but there is no gray elephant in Pacific',
            'Has you correctly write the URL?',
            'Go home you are drunk !!!',
        ]
        message_index = random.randrange(0,len(error_messages))
        error_message = error_messages[message_index]
        data = {
           'error_title'  : '404, Page not found',
           'error_message' : error_message,
        }
        return template('example/error', data = data)
    
    @error(403)
    def _error_403(error):
        import random
        error_messages = [
            'You have just landed at area 51',
            'No, you cannot access this, Cowboy !!!',
            'Restricted, you must be 200 years old to access this page',
        ]
        message_index = random.randrange(0,len(error_messages))
        error_message = error_messages[message_index]
        data = {
           'error_title'  : '403, Forbidden',
           'error_message' : error_message,
        }
        return template('example/error', data = data)
    
    @error(500)
    def _error_500(error):
        import random
        error_messages = [
            'Something goes wrong',
            'No no no... Not again...',
            'Congratulation, you have just found an error !!!',
        ]
        message_index = random.randrange(0,len(error_messages))
        error_message = error_messages[message_index]
        data = {
           'error_title'  : '500, Internal Server Error',
           'error_message' : error_message,
        }
        return template('example/error', data = data)