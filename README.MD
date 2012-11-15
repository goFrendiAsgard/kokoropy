Kokoropy
=========

A python web framework, from my heart <3

In japanese, kokoro means heart
I make kokoropy because I can't find any python web-framework which I really comfort with.

Kokoropy is pythonic, especially in these points:
* Explicit is better than implicit: kokoropy doesn't hide anything. 
* Simple is better than complex: kokoropy is made as simple as possible. 

Kokoropy is not too pythonic, especially in these points:
* There should be one-- and preferably only one --obvious way to do it: although kokoropy encourage OOP approach, but procedural approach is still work

Other things about kokoropy:

* Based on Bottlepy
* It is portable
* You need to restart the server everytime changing any code (just like django), and actually I hate this way :p
* It is under-development : don\'t use it for production purpose!
* Inspired by several PHP frameworks
	- The "action_" prefix for every published function in controller is inspired by laravel and FuelPHP
	- MVC approach will be as simple as CodeIgniter

How to use
--------------

* Go to kokoropy/app, you can make a new application by creating a python package (a directory with empty __init__.py)
* Inside your application, make a new python package named controllers. Until this point you will have something like kokoropy/app/your_app/controllers
* Inside you controllers, make a python module (a file with .py extension). Let's name it main.py
* If you prefer procedural approach (personally I suggest you to use OOP approach, but there is nothing wrong with procedural approach), write this script:

```python
def action_index(name='Stranger'):
    return 'Hello world, nice to meet you '+name
```

* If you prefer OOP approach, make a Main class (the name should be \"Main\"):

```python
class Main(object):
    def action_index(self, name='Stranger'):
        return 'Hello world, nice to meet you '+name
```

* Edit the configuration as you wish (or just leave it as it is), you can find the configuration file in kokoropy/config.py
* Go to kokoropy directory, start the server 

```python
 python start.py
```

* Access your first application via browser (http://localhost:8080/your_app/main/index/aragorn).
  This will run action_index function and pass aragorn as name parameter in your_app/main.py
