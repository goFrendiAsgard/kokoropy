from kokoropy import template, request, response

class Default_Controller(object):
    def action_index(self):
        from applications.test.models.test_model import test_things
        test_things()
        return 'look at log'

    def action_set_cookie(self):
        # Juno is cookie name
        # Minerva is the value
        # Aphrodite is the secret
        response.set_cookie('Juno', 'Minerva', 'Aphrodite')

    def action_get_cookie(self):
        return request.get_cookie('Juno', 'x', 'Aphrodite')