#####################################################################################
# Configuration name   : FIRST_TIME
# Default value        : True
# Alternative value    : True, False
# If you have modify something, and want to disable kokoropy's default home page, 
# just set this to False
#####################################################################################
FIRST_TIME = True

#####################################################################################
# Configuration name   : CUSTOM_ERROR
# Default value        : False
# Alternative value    : True, False
# If you want to enable custom error, end let your visitor see the 
# sarcastic-human word instead of any informative-for-developer-info 
# such as "404 Not found", set this to true
#####################################################################################
CUSTOM_ERROR = False

#####################################################################################
# End of configuration
#####################################################################################

from kokoropy import load_view, base_url

################### These functions are used for routes (url) #######################
def index():
    return load_view('index', 'index.html', active_page = 'home')

def getting_started():
    return load_view('index', 'getting_started.html', active_page = 'getting_started')

####################### These functions are used for hooks ##########################
def before_request():
    pass

def after_request():
    pass

####################### These functions are used for errors #########################
def error_404(error):
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
    return load_view('index','error', data = data)

def error_403(error):
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
    return load_view('index','error', data = data)

def error_500(error):
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
    return load_view('index','error', data = data)

if FIRST_TIME:
    urls = (
       # index
       ('/', index),
       (base_url(), index),
       # getting_started
       (base_url('getting_started'), getting_started)
    )

if CUSTOM_ERROR:
    hooks = (
       ('before_request', before_request),
       ('after_request', after_request)
    )
    
    errors = (
       ('404', error_404),
       ('403', error_403),
       ('500', error_500)
    )
