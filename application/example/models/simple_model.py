class Simple_Model(object):
    """
    A very simple model.
    """

    def say_hello(self, name=None):
        if name is None:
            return "Hello Stranger"
        else:
            return "Hello "+name