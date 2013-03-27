class Simple_Model(object):

    def say_hello(self, name=None):
        if name is None:
            return "Hello Stranger"
        else:
            return "Hello "+name