from kokoropy import var_dump

class Human:
    def __init__(self):
        self.name = 'Clark'
        self.hobby = ['fishing', 'flying']
        self.label = ('man of steel', 'superman')
        self.other_property = {'last_name' : 'Kent'}
        
    def fly(self):
        print('Up up and away')

def function():
    pass

data = {
        'class' : Human,
        'instance': Human(),
        'list' : [1,2,3,4,5],
        'dict': {'instance': Human()},
        'function' : function,
        'None' : function(),
        'Float' : 3.5,
        'Boolean' : False
    }

var_dump(print_output=True)
var_dump(print_output=True, mode='html')
var_dump(print_output=True, mode='console')