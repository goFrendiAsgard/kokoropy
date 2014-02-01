from kokoropy import template, request, os, redirect, base_url, save_uploaded_asset, remove_asset,\
    Autoroute_Controller, load_view, load_model
import random, hashlib

class Default_Controller(Autoroute_Controller):
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
        Simple_Model = load_model('example', 'simple_model')
        DB_Model = load_model('example', 'db_model')
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
        message = say_hello+', the session said that you have visit routing demo page '+str(request.SESSION['counter'])+' times'
        return load_view('example', 'recommended_hello', message=message)
    
    def generate_private_code(self):
        num = random.random()
        private_code = str(hashlib.md5(str(num)))
        request.SESSION['__private_code'] = private_code
        return private_code
    
    def action_pokemon(self, keyword=None):
        """
        GET, POST & parameter usage example.
        This function is automatically routed to: http://localhost:8080/example/recommended/pokemon/parameter
        """
        # get keyword
        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
        elif 'keyword' in request.POST:
            keyword = request.POST['keyword']
        if keyword is None:
            keyword = ''
        
        # get action
        action = ''
        if 'action' in request.POST:
            action = request.POST['action']
        
        # get data
        private_code = ''
        pokemon_id = ''
        pokemon_name = ''        
        if 'pokemon_id' in request.POST:
            pokemon_id = request.POST['pokemon_id']
        if 'pokemon_name' in request.POST:
            pokemon_name = request.POST['pokemon_name']
        
        # rely on private_code and keep calm on accidental refresh
        if '__private_code' in request.POST:
            private_code = request.POST['__private_code']
        elif '__private_code' in request.GET:
            private_code = request.GET['__private_code']
        
        # do the action
        if '__private_code' in request.SESSION and private_code == request.SESSION['__private_code']:
            # upload image
            if action == 'add' or action == 'edit':
                pokemon_image = self.upload_image()
            # save the data
            if action == 'add':
                self.db_model.insert_pokemon(pokemon_name, pokemon_image)
            elif action == 'edit':
                self.db_model.update_pokemon(pokemon_id, pokemon_name, pokemon_image)
            elif action == 'delete':
                row = self.db_model.get_pokemon_by_id(pokemon_id)
                if row != False:
                    image = row['image']
                    remove_asset(os.path.join('uploads', image), 'example')
                self.db_model.delete_pokemon(pokemon_id)
        
        private_code = self.generate_private_code()
        # get pokemons
        pokemons = self.db_model.get_pokemon(keyword)
        return load_view('example', 'pokemon_view', pokemons=pokemons, __private_code = private_code)
    
    def action_form_add_pokemon(self):
        private_code  = self.generate_private_code()
        return load_view('example', 'pokemon_add_form', __private_code = private_code)
    
    def action_form_edit_pokemon(self, pokemon_id):
        pokemon = self.db_model.get_pokemon_by_id(pokemon_id)
        private_code  = self.generate_private_code()
        return load_view('example','pokemon_edit_form', pokemon=pokemon, __private_code = private_code)
        
    # not routed    
    def upload_image(self):
        upload =  request.files.get('pokemon_image')
        if upload is None:
            return ''
        else:
            name, ext = os.path.splitext(upload.filename)
            if ext not in ('.png','.jpg','.jpeg'):
                return ''
            # appends upload.filename automatically
            if save_uploaded_asset('pokemon_image', path='uploads', application_name='example'):
                return name+ext
            else:
                return ''