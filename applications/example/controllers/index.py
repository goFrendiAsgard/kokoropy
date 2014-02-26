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
        import matplotlib.pyplot as plt
        # determine x, sin(x) and cos(x)
        x = np.arange(0, max_range, 0.1)
        y1 = np.sin(x)
        y2 = np.cos(x)
        # make figure
        fig = plt.figure()
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
                        numeric_value[caption][row[i]] = float(len(numeric_value[caption]))
                    row[i] = numeric_value[caption][row[i]]
                row[i] = float(row[i]) # ensure this is float
            while len(row)<len(caption_list):
                row.append(0)
            data.append(row[:-1])
            target.append(row[-1])
        data = array(data)
        target = array(target)
        return (data, target, caption_list, numeric_value)
    
    def action_classification_result(self):
        import json
        import numpy as np
        import matplotlib.pyplot as plt
        import time
        
        result = {
                  'success' : True,
                  'message' : ''
            }
        # redirect if data not completed
        if 'training_csv' not in request.POST or 'classifier' not in request.POST:
            result['message'] = 'Undefined training data, testing data, or classifier'
            result['success'] = False
            return json.dumps(result)
            
        # preprocess POST data
        training_csv = request.POST['training_csv']
        if 'testing_csv' not in request.POST or request.POST['testing_csv'] == '':
            testing_csv =  '\n'.join(training_csv.split('\n')[1:])
        else:
            testing_csv = request.POST['testing_csv']
        classifier_name = request.POST['classifier']
        parameter_pair_list = []
        for parameter in self.classifiers[classifier_name]:
            value = request.POST['param_'+parameter]
            if (not self.is_number(value)) and value != 'True' and value != 'False' and value != 'None':
                value = '"'+value.replace('"','\"')+'"'
            parameter_pair_list.append(parameter + ' = ' + value)
        parameter_string = ", ".join(parameter_pair_list)
        
        if training_csv == '':
            result['message'] = 'Training data is empty'
            result['success'] = False
            return json.dumps(result)
        
        # preprocess csv
        try:
            training_data, training_target, caption_list, numeric_value = self.extract_csv(training_csv)
            testing_data, testing_target, caption_list, numeric_value = self.extract_csv(testing_csv, caption_list, numeric_value)
            if 'predict_csv' in request.POST and request.POST['predict_csv'] != '' :
                do_prediction = True
                predict_csv = request.POST['predict_csv']
                prediction_data, prediction_target, caption_list, numeric_value = self.extract_csv(predict_csv, caption_list, numeric_value)
                prediction_data = self.csv_to_list(predict_csv)
                del prediction_target
            else:
                do_prediction = False
                prediction_data = []
        except Exception, e:
            result['success'] = False
            result['message'] = 'Unexpected error while extracting csv : '+ e.message
        if not result['success']:
            return json.dumps(result)
        
        # make classifier
        classifier = None
        try:
            import_module_name = '.'.join(classifier_name.split('.')[:-1])
            exec('import '+import_module_name)
            exec('classifier = '+classifier_name+'('+parameter_string+')')
        except Exception, e:
            result['success'] = False
            result['message'] = 'Unexpected error while define classifier : '+ e.message
        if not result['success']:
            return json.dumps(result)
        
        # learn
        try:
            classifier.fit(training_data, training_target)
        except Exception, e:
            result['success'] = False
            result['message'] = 'Unexpected error while fit classifier : '+ e.message
        if not result['success']:
            return json.dumps(result)
        
        # and test the classifier
        try:
            training_predict_target = classifier.predict(training_data)
            testing_predict_target = classifier.predict(testing_data)
            if do_prediction:
                prediction_predict_target = classifier.predict(prediction_data)
            else:
                prediction_predict_target = []
        except Exception, e:
            result['success'] = False
            result['message'] = 'Unexpected error while predicting target : '+ e.message
        if not result['success']:
            return json.dumps(result)
        
        # if the classes is not in numeric value, then use_alias = True
        use_alias = caption_list[-1] in numeric_value
        target_dict = {}
        if use_alias:
            target_numeric_value = numeric_value[caption_list[-1]]
            for label in target_numeric_value:
                target_dict[target_numeric_value[label]] = label
        
        # Available classes
        groups = []
        for target in (training_target, testing_target):
            for i in xrange(len(target)):
                if target[i] not in groups:
                    groups.append(target[i])
        
        # plotting
        dimensions = caption_list[:-1]
        dimension_count = len(dimensions)
        subplot_num = dimension_count * (dimension_count-1)
        for i in xrange(dimension_count):
            subplot_num -= i
        if subplot_num == 1:
            row_count = 1
            col_count = 1
        else:
            row_count = np.ceil(subplot_num / 2)
            col_count = 2
        # determine x, sin(x)
        x = np.arange(0, 6.28, 0.1)
        y = np.sin(x)
        # make figure
        fig = plt.figure(figsize=(20.0, 12.0))
        fig.subplots_adjust(hspace = 0.5, wspace = 0.5)
        fig.suptitle('Dimension Projection')
        # subplot
        subplot_index = 1
        second_dimension_start_index = 1
        first_dimension_index = 0
        for first_dimension in dimensions:
            second_dimension_index = second_dimension_start_index
            for second_dimension in dimensions[second_dimension_start_index:]:
                ax = fig.add_subplot(row_count, col_count, subplot_index)
                ax.plot(x, y, 'b')
                ax.plot(x, y, 'ro')
                ax.set_title ('y and x')
                ax.set_xlabel(first_dimension)
                ax.set_ylabel(second_dimension)
                subplot_index += 1
                second_dimension_index += 1
            first_dimension_index += 1
            second_dimension_start_index += 1
        # make canvas
        file_name = 'plot_'+str(np.random.randint(10000))+str(time.time())+'.png'
        plot_url = draw_matplotlib_figure(fig,file_name,'example')
        
        # initiate false positive, false negative, true positive, and true negative
        training_false_positive = {}
        training_false_negative = {}
        training_true_positive = {}
        training_true_negative = {}
        testing_false_positive = {}
        testing_false_negative = {}
        testing_true_positive = {}
        testing_true_negative = {}
        for group in groups:
            training_false_positive[group] = 0.0
            training_false_negative[group] = 0.0
            training_true_positive[group] = 0.0
            training_true_negative[group] = 0.0
            testing_false_positive[group] = 0.0
            testing_false_negative[group] = 0.0
            testing_true_positive[group] = 0.0
            testing_true_negative[group] = 0.0
        # determine true positive, true negative, false positive and false negative for training and testing
        for i in xrange(len(training_target)):
            for group in groups:
                if training_target[i] == group and training_predict_target[i] == group:
                    training_true_positive[group] += 1
                elif training_target[i] != group and training_predict_target[i] != group:
                    training_true_negative[group] += 1
                elif training_target[i] != group and training_predict_target[i] == group:
                    training_false_positive[group] += 1
                else:
                    training_false_negative[group] += 1
        for i in xrange(len(testing_target)):
            for group in groups:
                if testing_target[i] == group and testing_predict_target[i] == group:
                    testing_true_positive[group] += 1
                elif testing_target[i] != group and testing_predict_target[i] != group:
                    testing_true_negative[group] += 1
                elif testing_target[i] != group and testing_predict_target[i] == group:
                    testing_false_positive[group] += 1
                else:
                    testing_false_negative[group] += 1
        
        # use alias if needed        
        if use_alias:
            groups = []
            for key in target_dict:
                label = target_dict[key]
                groups.append(label)
                training_true_positive[label] = training_true_positive[key]
                training_true_positive.pop(key)
                training_true_negative[label] = training_true_negative[key]
                training_true_negative.pop(key)
                training_false_positive[label] = training_false_positive[key]
                training_false_positive.pop(key)
                training_false_negative[label] = training_false_negative[key]
                training_false_negative.pop(key)
                testing_true_positive[label] = testing_true_positive[key]
                testing_true_positive.pop(key)
                testing_true_negative[label] = testing_true_negative[key]
                testing_true_negative.pop(key)
                testing_false_positive[label] = testing_false_positive[key]
                testing_false_positive.pop(key)
                testing_false_negative[label] = testing_false_negative[key]
                testing_false_negative.pop(key)
            # prediction
            str_prediction_predict_target = []
            for i in xrange(len(prediction_predict_target)):
                str_prediction_predict_target.append(target_dict[prediction_predict_target[i]])
            prediction_predict_target = str_prediction_predict_target
        
        # further calculation (http://en.wikipedia.org/wiki/Accuracy_and_precision)
        total_false_positive = {}
        total_false_negative = {}
        total_true_positive = {}
        total_true_negative = {}
        training_sensitivity = {}
        training_specificity = {}
        training_precision = {}
        training_negative_predictive_value = {}
        training_accuracy = {}
        training_balanced_accuracy = {}
        training_informedness = {}
        testing_sensitivity = {}
        testing_specificity = {}
        testing_precision = {}
        testing_negative_predictive_value = {}
        testing_accuracy = {}
        testing_balanced_accuracy = {}
        testing_informedness = {}
        total_sensitivity = {}
        total_specificity = {}
        total_precision = {}
        total_negative_predictive_value = {}
        total_accuracy = {}
        total_balanced_accuracy = {}
        total_informedness = {}
        for group in groups:
            # total true and false positive and negative
            total_false_positive[group] = training_false_positive[group] + testing_false_positive[group]
            total_false_negative[group] = training_false_negative[group] + testing_false_negative[group]
            total_true_positive[group] = training_true_positive[group] + testing_true_positive[group]
            total_true_negative[group] = training_true_negative[group] + testing_true_negative[group]
            
            # training measurement
            #   sensitivity
            if (training_true_positive[group] + training_false_negative[group]) == 0:
                training_sensitivity[group] = 0
            else:
                training_sensitivity[group] = training_true_positive[group] / (training_true_positive[group] + training_false_negative[group])
            #   specificity
            if (training_true_negative[group] + training_false_positive[group]) == 0:
                training_specificity[group] = 0
            else:
                training_specificity[group] = training_true_negative[group] / (training_true_negative[group] + training_false_positive[group])
            #   precision
            if (training_true_positive[group] + training_false_positive[group]) == 0:
                training_precision[group] = 0
            else:
                training_precision[group] = training_true_positive[group] / (training_true_positive[group] + training_false_positive[group])
            #   negative prediction value
            if (training_true_negative[group] + training_false_negative[group]) == 0:
                training_negative_predictive_value[group] = 0
            else:
                training_negative_predictive_value[group] = training_true_negative[group] / (training_true_negative[group] + training_false_negative[group])
            #   accuracy
            if (training_true_positive[group] + training_true_negative[group] + training_false_positive[group] + training_false_negative[group]) == 0:
                training_accuracy[group] = 0
            else:
                training_accuracy[group] = (training_true_positive[group] + training_true_negative[group]) / (training_true_positive[group] + training_true_negative[group] + training_false_positive[group] + training_false_negative[group])
            #   balanced accuracy
            training_balanced_accuracy[group] = (training_sensitivity[group] + training_specificity[group])/2.0
            #   informedness
            training_informedness[group] = training_sensitivity[group] + training_specificity[group] - 1
            
            # testing measurement
            #   sensitivity
            if (testing_true_positive[group] + testing_false_negative[group]) == 0:
                testing_sensitivity[group] = 0
            else:
                testing_sensitivity[group] = testing_true_positive[group] / (testing_true_positive[group] + testing_false_negative[group])
            #   specificity
            if (testing_true_negative[group] + testing_false_positive[group]) == 0:
                testing_specificity[group] = 0
            else:
                testing_specificity[group] = testing_true_negative[group] / (testing_true_negative[group] + testing_false_positive[group])
            #   precision
            if (testing_true_positive[group] + testing_false_positive[group]) == 0:
                testing_precision[group] = 0
            else:
                testing_precision[group] = testing_true_positive[group] / (testing_true_positive[group] + testing_false_positive[group])
            #   negative prediction value
            if (testing_true_negative[group] + testing_false_negative[group]) == 0:
                testing_negative_predictive_value[group] = 0
            else:
                testing_negative_predictive_value[group] = testing_true_negative[group] / (testing_true_negative[group] + testing_false_negative[group])
            #   accuracy
            if (testing_true_positive[group] + testing_true_negative[group] + testing_false_positive[group] + testing_false_negative[group]) == 0:
                testing_accuracy[group] = 0
            else:
                testing_accuracy[group] = (testing_true_positive[group] + testing_true_negative[group]) / (testing_true_positive[group] + testing_true_negative[group] + testing_false_positive[group] + testing_false_negative[group])
            #   balanced accuracy
            testing_balanced_accuracy[group] = (testing_sensitivity[group] + testing_specificity[group])/2.0
            #   informedness
            testing_informedness[group] = testing_sensitivity[group] + testing_specificity[group] - 1
            
            # total measurement
            #   sensitivity
            if (total_true_positive[group] + total_false_negative[group]) == 0:
                total_sensitivity[group] = 0
            else:
                total_sensitivity[group] = total_true_positive[group] / (total_true_positive[group] + total_false_negative[group])
            #   specificity
            if (total_true_negative[group] + total_false_positive[group]) == 0:
                total_specificity[group] = 0
            else:
                total_specificity[group] = total_true_negative[group] / (total_true_negative[group] + total_false_positive[group])
            #   precision
            if (total_true_positive[group] + total_false_positive[group]) == 0:
                total_precision[group] = 0
            else:
                total_precision[group] = total_true_positive[group] / (total_true_positive[group] + total_false_positive[group])
            #   negative prediction value
            if (total_true_negative[group] + total_false_negative[group]) == 0:
                total_negative_predictive_value[group] = 0
            else:
                total_negative_predictive_value[group] = total_true_negative[group] / (total_true_negative[group] + total_false_negative[group])
            #   accuracy
            if (total_true_positive[group] + total_true_negative[group] + total_false_positive[group] + total_false_negative[group]) == 0:
                total_accuracy[group] = 0
            else:
                total_accuracy[group] = (total_true_positive[group] + total_true_negative[group]) / (total_true_positive[group] + total_true_negative[group] + total_false_positive[group] + total_false_negative[group])
            #   balanced accuracy
            total_balanced_accuracy[group] = (total_sensitivity[group] + total_specificity[group])/2.0
            #   informedness
            total_informedness[group] = total_sensitivity[group] + total_specificity[group] - 1
            
        # show it
        result = {
                  'success' : True,
                  'message' : '',
                  'groups' : groups,
                  'training_true_positive' : training_true_positive,
                  'training_true_negative' : training_true_negative,
                  'training_false_positive': training_false_positive,
                  'training_false_negative': training_false_negative,
                  'testing_true_positive'  : testing_true_positive,
                  'testing_true_negative'  : testing_true_negative,
                  'testing_false_positive' : testing_false_positive,
                  'testing_false_negative' : testing_false_negative,
                  'total_true_positive'    : total_true_positive,
                  'total_true_negative'    : total_true_negative,
                  'total_false_positive'   : total_false_positive,
                  'total_false_negative'   : total_false_negative,
                  'training_sensitivity' : training_sensitivity,
                  'testing_sensitivity'  : testing_sensitivity,
                  'total_sensitivity'    : total_sensitivity,
                  'training_specificity' : training_specificity,
                  'testing_specificity'  : testing_specificity,
                  'total_specificity'    : total_specificity,
                  'training_precision' : training_precision,
                  'testing_precision'  : testing_precision,
                  'total_precision'    : total_precision,
                  'training_negative_predictive_value' : training_negative_predictive_value,
                  'testing_negative_predictive_value'  : testing_negative_predictive_value,
                  'total_negative_predictive_value'    : total_negative_predictive_value,
                  'training_accuracy' : training_accuracy,
                  'testing_accuracy'  : testing_accuracy,
                  'total_accuracy'    : total_accuracy,
                  'training_balanced_accuracy' : training_balanced_accuracy,
                  'testing_balanced_accuracy'  : testing_balanced_accuracy,
                  'total_balanced_accuracy'    : total_balanced_accuracy,
                  'training_informedness' : training_informedness,
                  'testing_informedness'  : testing_informedness,
                  'total_informedness'    : total_informedness,
                  'do_prediction'         : do_prediction,
                  'prediction_data'       : prediction_data,
                  'prediction_result'     : prediction_predict_target,
                  'plot_url'              : plot_url
            }
        return json.dumps(result)
            