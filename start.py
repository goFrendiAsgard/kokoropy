'''
Created on Nov 13, 2012

@author: gofrendi
'''
# register every package and modules in this directory
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

# import modules
import config
import kokoropy.bottle as bottle

def run_function(application, controller, function, params=[]):
    '''
    return (error, result)
    error : boolean, error status
    result: value returned by the function
    If there is no function found, we will look for the same function in the Main class of the controller
    '''
    # change params into comma separated string
    if len(params) == 0:
            params = ''
    else:
        for i in xrange(len(params)):
            params[i] = "'"+str(params[i])+"'"
        params = ','.join(params)
    
    # just like laravel or fuelPHP, it is better to have "action_" prefix for every
    # published function
    function = 'action_'+function
    
    # default error and result. I always prepared for the worst :)
    result = ''
    error = True
    # the sandbox to run the program
    sandbox = {}
    try:
        # import controller module
        exec('import app.'+application+'.controllers.'+controller+' as controller_module') in sandbox
        try:
            # assuming the controller module has the function (procedural approach)            
            exec('result = controller_module.'+function+'('+params+')') in sandbox
        except:
            # assuming the controller module has the class (object oriented approach)
            exec('controller_object = controller_module.Main()') in sandbox
            exec('result = controller_object.'+function+'('+params+')') in sandbox
        result = sandbox['result']
        error = False           
    except:
        error = True
    # delete the sandbox
    del(sandbox)
    return (error, result)

def load(url):
    '''
    return (error, result)
    error : boolean, error status
    result: value returned by the url
    '''
    # split url into list
    parts = []
    if type(url) is str:
        parts = url.split('/')
        
    # default config value
    default_application = config.default_application
    default_controller = 'main'
    default_function = 'index' # the real function name in your controller should be action_index
    
    # default error and result. I always prepared for the worst :)
    error = True
    result = ''    
    
    if len(parts)>=3:
        # complete scenario
        error, result = run_function(parts[0], parts[1], parts[2], parts[3:])
        if not error:
            return (error, result)    
    
    if len(parts)>=2:
        # default function scenario
        error, result = run_function(parts[0], parts[1], default_function, parts[2:])
        if not error:
            return (error, result)    
    
    if len(parts)>=1:
        # default function and default controller scenario
        error, result = run_function(parts[0], default_controller, default_function, parts[1:])
        if not error:
            return (error, result)
    
    # minimum scenario
    error, result = run_function(default_application, default_controller, default_function, parts)
    if not error:
        return (error, result)
    
    return (error, result)

@bottle.route('/')
@bottle.route('/<url:path>', method='post')
@bottle.route('/<url:path>', method='get')
def init(url=None):     
    # load url
    error, result = load(url)
    if error:
        return 'kokoro routing error'
    else:
        return result

if __name__ == '__main__':
    bottle.run(host=config.host, port=config.port, debug=config.debug, reloader=config.reloader)