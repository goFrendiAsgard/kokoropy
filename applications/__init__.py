from kokoropy import template, error, hook

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
