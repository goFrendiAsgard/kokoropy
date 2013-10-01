from kokoropy import template

class Default_Controller(object):
    def action_index(self):
        from applications.test.models.test_model import test_things
        test_things()
        return 'look at log'