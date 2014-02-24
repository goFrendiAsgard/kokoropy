from kokoropy import request, draw_matplotlib_figure, Autoroute_Controller, \
    load_view, save_uploaded_asset, remove_asset, redirect
import random, hashlib, os
from kokoropy.kokoro import base_url

class My_Controller(Autoroute_Controller):
    '''
    Example collections
    '''
    
    def __init__(self):
        # load databases for most of example
        from ..models.db_model import Db_Model
        self.db_model = Db_Model()
        # classifiers for classification
        self.classifiers = {
                'sklearn.neighbors.KNeighborsClassifier' : {
                        'n_neighbors' : 5,
                    },
                'sklearn.svm.SVC'  : {
                        'C'           : 0.025,
                        'kernel'      : 'linear',
                        'gamma'       : 2
                    },
                'sklearn.tree.DecisionTreeClassifier' : {
                        'max_depth'   : 5
                    },
                'sklearn.naive_bayes.GaussianNB' : {
                    },
                'sklearn.dummy.DummyClassifier' : {
                        'strategy'    : 'stratified', 
                        'random_state': 'None'
                    },
                'sklearn.ensemble.RandomForestClassifier' : {
                        'n_estimators':10,
                        'criterion':'gini',
                        'max_depth': 'None',
                        'min_samples_split':2,
                        'min_samples_leaf':1,
                        'max_features':'auto',
                        'bootstrap':'True',
                        'oob_score':'False',
                        'n_jobs':1,
                        'random_state':'None',
                        'verbose':0,
                        'min_density':'None',
                        'compute_importances':'None'
                    }
            }
    
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
    
    def action_classification(self):
        return load_view('example', 'classification', classifiers = self.classifiers)
    
    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def csv_to_list(self, str_csv):
        '''
        change csv string to python list
        '''
        import StringIO, csv
        f = StringIO.StringIO(str_csv)
        reader = csv.reader(f, delimiter = ',')
        lst = []
        for row in reader:
            lst.append(row)
        return lst
    
    def extract_csv(self, csv, caption_list= None, numeric_value={}):
        '''
        return tuples contains data, target, caption_list and numeric_value
            data is 2D array, needed for sklearn's classifier fit/predict function
            target is 1D array, needed for sklearn's classifier fit/predict function
            caption_list is array of string, contains human-readable caption (1st row of csv)
            numeric_value is a dictionary, contains captions and numbers
        '''
        from numpy import array
        data_list = self.csv_to_list(csv)
        if caption_list is None:
            caption_list = data_list[0]
            data_list = data_list[1:]
        data = []
        target = []
        for row in data_list:
            for i in xrange(len(row)):
                if not self.is_number(row[i]):
                    caption = caption_list[i]
                    if caption not in numeric_value:
                        numeric_value[caption] = {}
                    if row[i] not in numeric_value[caption]:
                        numeric_value[caption][row[i]] = len(numeric_value[caption])
                    row[i] = numeric_value[caption][row[i]]
                row[i] = float(row[i]) # ensure this is float
            data.append(row[:-1])
            target.append(row[-1])
        data = array(data)
        target = array(target)
        return (data, target, caption_list, numeric_value)
    
    def action_classification_result(self):
        # redirect if data not completed
        if 'training_csv' not in request.POST or 'testing_csv' not in request.POST or 'classifier' not in request.POST:
            redirect(base_url('example/classification'))
            
        # preprocess POST data
        training_csv = request.POST['training_csv']
        testing_csv = request.POST['testing_csv']
        classifier_name = request.POST['classifier']
        parameter_pair_list = []
        for parameter in self.classifiers[classifier_name]:
            value = request.POST['param_'+parameter]
            if (not self.is_number(value)) and value != 'True' and value != 'False' and value != 'None':
                value = '"'+value.replace('"','\"')+'"'
            parameter_pair_list.append(parameter + ' = ' + value)
        parameter_string = ", ".join(parameter_pair_list)
        print parameter_string
        
        if training_csv == '' or testing_csv == '':
            redirect(base_url('example/classification'))
        
        # preprocess csv
        training_data, training_target, caption_list, numeric_value = self.extract_csv(training_csv)
        testing_data, testing_target, caption_list, numeric_value = self.extract_csv(testing_csv, caption_list, numeric_value)
        # make classifier
        classifier = None
        import_module_name = '.'.join(classifier_name.split('.')[:-1])
        exec('import '+import_module_name)
        exec('classifier = '+classifier_name+'('+parameter_string+')')
        classifier.fit(training_data, training_target)
        predict_target = classifier.predict(testing_data)
        
        # show the result
        true_count = 0.0
        false_count = 0.0
        for i in xrange(len(predict_target)):
            if predict_target[i] == testing_target[i]:
                true_count += 1
            else:
                false_count += 1
        accuracy = true_count/(false_count+true_count) * 100
        return 'True : '+str(true_count)+', False : '+str(false_count)+', Accuracy : '+str(accuracy)+'%';