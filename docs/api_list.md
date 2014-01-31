* `request.GET`

* `request.POST`

* `request.SESSION`

* `request.HOST`

* `class KokoroWSGIRefServer(bottle.ServerAdapter)`
    
    Currently is the same to bottle default WSGIServer, nothing added

* `def template(*args, **kwargs)`
    
    Override bottle's template function, add BASE_URL, RUNTIME_PATH, and APPLICATION_PATH to the kwargs, so that those values accessible in template file

* `def load_model(application_name, model_name, object_name = None)`
    
    Return `object_name` in your `model_name` model of your `application_name` application

* `def load_controller(application_name, controller_name, function_or_class)`
    
    Return `object_name` in your `model_name` model of your `application_name` application

* `def load_view(application_name, view_name, *args, **kwargs)`
    
    Wrapper for bottle's template function

* `def isset(variable)`
    
    PHP favored isset. Usage: isset("a_variable_name")

* `def add_trailing_slash(string)`
    
    Add trailing slash

* `def remove_trailing_slash(string)`
    
    Remove trailing slash

* `def add_begining_slash(string)`
    
    Add begining slash

* def remove_begining_slash(string):
    
    Remove beginning slash

* `def runtime_path(path='')`
    
    Get runtime path or path relative to runtime path

* `def application_path(path='')`
    
    Get application path or path relative to application path

* `def base_url(url='')`
    
    Get base url or path relative to base url 

* `def rmtree(path, ignore_errors=False, onerror=None)`
    
    Wrapper for `shutil.rmtree`

* `def copytree(src, dst, symlinks=False, ignore=None)`
    
    Enchanced version of `shutil.copytree`, this function will make destination folder if it is not exists

* `def kokoro_init(**kwargs)`
    
    Start kokoropy

* `def draw_matplotlib_figure(figure)`
    
    Draw matplotlib figure

* `def save_uploaded_asset(upload_key_name, path='', application_name='index')`
    
    Upload the asset

* `def remove_asset(path, application_name='index')`
    
    Remove the asset