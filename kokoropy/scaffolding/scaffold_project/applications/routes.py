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
