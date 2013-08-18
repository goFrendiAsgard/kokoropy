from kokoropy import template, request, os, base_url

class Default_Controller(object):
    """
     RECOMMENDED APPROACH (Automagically route) 
    
     An OOP Style with automatic routing example (just like CodeIgniter or FuelPHP)
     The routing will be done automatically.
     To use this feature:
        * The controller file name can be anything, and will be used for routing
        * Your controller class name should be "Default_Controller"
        * Your published method should have "action" prefix
        * The published URL would be 
          http://localhost:8080/app_dir/controller_file/published_method/params
        * If your app_dir, controller_file or published_method named "index", it can be
          omitted
        * For convention, this is the recommended way to do it    
    """
    
    def __init__(self):
        # import models
        from applications.example.models.simple_model import Simple_Model
        from applications.example.models.db_model import DB_Model
        # make instance of models      
        self.simple_model = Simple_Model()
        self.db_model = DB_Model()
    
    def action_index(self, name=None):
        """
        Session usage example.
        This function is automatically routed to: http://localhost:8080/example/recommended/index/parameter
        """
        # get counter from SESSION, or set it
        if 'counter' in request.SESSION:
            request.SESSION['counter'] += 1
        else:
            request.SESSION['counter'] = 1
        # get say_hello
        say_hello = self.simple_model.say_hello(name)
        message = say_hello+', you have visit this page '+str(request.SESSION['counter'])+' times'
        return template('example/recommended_hello', message=message)
    
    def action_pokemon(self, keyword=None):
        """
        GET, POST & parameter usage example.
        This function is automatically routed to: http://localhost:8080/example/recommended/pokemon/parameter
        """
        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
        elif 'keyword' in request.POST:
            keyword = request.POST['keyword']
        if keyword is None:
            keyword = ''
        # get pokemons
        pokemons = self.db_model.get_pokemon(keyword)
        return template('example/pokemon', pokemons=pokemons)
    
    def action_upload(self):        
        """
        File Upload example.
        This function is automatically routed to: http://localhost:8080/example/recommended/upload
        """
        upload =  request.files.get('upload')
        if upload is None:
            return template('example/upload', message='upload image file (png, jpg or jpeg)')
        else:
            name, ext = os.path.splitext(upload.filename)
            if ext not in ('.png','.jpg','.jpeg'):
                return template('example/upload', message='invalid file extension '+ext)
            # appends upload.filename automatically
            upload_path = os.path.dirname(os.path.dirname(__file__))+'/assets/uploads/'
            upload.save(upload_path) 
            return template('example/upload', message='upload '+name+ext+' success')
    
    # not routed
    def unpublished_function(self):
        return 'this is not published'