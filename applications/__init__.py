from kokoropy import template, error, hook
'''
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
        'Sorry, but there is no such a gray elephant in Atlantic...',
        'Are you sure that the page should be here? Well, in this case you are wrong',
        'Has you correctly write the URL?',
        'Go home you are drunk !!!',
        'It is not here, not here, not here... How many time should I tell you?',
        'Want the page to be exists? Hire us, and we will make one for you...',
        'Why do you look for something never exists? Please be realistic',
    ]
    message_index = random.randrange(0,len(error_messages))
    error_message = error_messages[message_index]
    data = {
       'error_title'  : '404, Page not found',
       'error_message' : error_message,
       'error' : error
    }
    return template('example/error', data = data)

@error(403)
def _error_403(error):
    import random
    error_messages = [
        'You are not authorized to enter ladies rest room, go out....',
        'You have landed at area 51. The MIB told us to not show the page',
        'Try to hack our site? We have record your IP Address and everything else',
        'What do you do here? Leave or die...',
    ]
    message_index = random.randrange(0,len(error_messages))
    error_message = error_messages[message_index]
    data = {
       'error_title'  : '403, Forbidden',
       'error_message' : error_message,
       'error' : error
    }
    return template('example/error', data = data)

@error(500)
def _error_500(error):
    import random
    error_messages = [
        'Right, right... It\'s not your fault it is our mistake',
        'Ouch,.. you have burn our hardisks. Be careful with what you click',
        'Do you notice that everytime you make our server error, a newborn baby will die...',
        'No no no... Not again...',
        'It is not our mistake, we have detect a bunch of ETI hacking our site',
    ]
    message_index = random.randrange(0,len(error_messages))
    error_message = error_messages[message_index]
    data = {
       'error_title'  : '500, Internal Server Error',
       'error_message' : error_message,
       'error' : error
    }
    return template('example/error', data = data)
'''