from kokoropy import request, draw_matplotlib_figure, Autoroute_Controller, \
    load_view, load_model, save_uploaded_asset, remove_asset
import random, hashlib, os

class My_Controller(Autoroute_Controller):
    '''
    Example collections
    '''
    
    def __init__(self):
        # import model
        DB_Model = load_model('example', 'db_model')
        self.db_model = DB_Model()
    
    def generate_private_code(self):
        """
        Simple trick to ensure that a POST request is only sent once
        """
        num = random.random()
        private_code = str(hashlib.md5(str(num)))
        request.SESSION['__private_code'] = private_code
        return private_code
    
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
    
    def action_index(self):
        return load_view('example', 'index')
    
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
                    image = row.image
                    remove_asset(os.path.join('uploads', image), 'example')
                self.db_model.delete_pokemon(pokemon_id)
        
        private_code = self.generate_private_code()
        # get pokemons
        pokemon_list = self.db_model.get_pokemon(keyword)
        return load_view('example', 'pokemon', pokemon_list=pokemon_list, __private_code = private_code)
    
    def action_form_add_pokemon(self):
        private_code  = self.generate_private_code()
        return load_view('example', 'pokemon_add_form', __private_code = private_code)
    
    def action_form_edit_pokemon(self, pokemon_id):
        pokemon = self.db_model.get_pokemon_by_id(pokemon_id)
        private_code  = self.generate_private_code()
        return load_view('example','pokemon_edit_form', pokemon=pokemon, __private_code = private_code)
    
    def action_plot(self):
        max_range = 6.28
        if 'range' in request.GET:
            max_range = float(request.GET['range'])
        # import things
        import numpy as np
        from matplotlib.figure import Figure
        # determine x, sin(x) and cos(x)
        x = np.arange(0, max_range, 0.1)
        y1 = np.sin(x)
        y2 = np.cos(x)
        # make figure       
        fig = Figure()
        fig.subplots_adjust(hspace = 0.5, wspace = 0.5)
        fig.suptitle('The legendary sine and cosine curves')
        # first subplot
        ax = fig.add_subplot(2, 1, 1)
        ax.plot(x, y1, 'b')
        ax.plot(x, y1, 'ro')
        ax.set_title ('y = sin(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        # second subplot
        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x, y2, 'b')
        ax.plot(x, y2, 'ro')
        ax.set_title ('y = cos(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        # make canvas
        return draw_matplotlib_figure(fig)
    
    def action_plotting(self):
        return load_view('example','plotting')