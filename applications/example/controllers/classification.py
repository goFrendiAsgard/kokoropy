from kokoropy import request, draw_matplotlib_figure, Autoroute_Controller, \
    load_view

class My_Controller(Autoroute_Controller):
    '''
    Example collections
    '''
    
    def __init__(self):
        # classifiers for classification
        self.classifiers = {
                'sklearn.neighbors.KNeighborsClassifier' : {
                        'n_neighbors' : 5,
                    },
                'sklearn.svm.SVC'  : {
                        'C'           : 1.0,
                        'kernel'      : 'rbf',
                        'degree'      : 3,
                        'gamma'       : 0.0,
                        'coef0'       : 0.0,
                        'shrinking'   : 'True',
                        'probability' : 'False',
                        'tol'         : 0.001,
                        'cache_size'  : 200,
                        'class_weight': 'None',
                        'verbose'     : 'False',
                        'max_iter'    : -1,
                        'random_state': 'None'
                    },
                'sklearn.svm.LinearSVC' : {
                        'penalty'     : 'l2',
                        'loss'        : 'l2',
                        'dual'        : 'True',
                        'tol'         : 0.0001,
                        'C'           : 1.0,
                        'multi_class' : 'ovr',
                        'fit_intercept' : 'True',
                        'intercept_scaling' : 1,
                        'class_weight' : 'None',
                        'verbose'      : 0,
                        'random_state' : 'None'
                    },
                'sklearn.tree.DecisionTreeClassifier' : {
                        'max_depth'   : 5
                    },
                'sklearn.naive_bayes.GaussianNB' : {
                    },
                'sklearn.naive_bayes.MultinomialNB' : {
                        'alpha'       : 1.0,
                        'fit_prior'   : 'True',
                        'class_prior' : 'None'
                    },
                'sklearn.naive_bayes.BernoulliNB' : {
                        'alpha'       : 1.0,
                        'binarize'    : 0.0,
                        'fit_prior'   : 'True',
                        'class_prior' : 'None',
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
                        'min_density':'0',
                        'compute_importances':'None'
                    }
            }

    def action_index(self):
        import json
        return load_view('example', 'classification', classifiers = self.classifiers, json_classifiers = json.dumps(self.classifiers))

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
        # preprocess str_csv
        data =  str_csv.split('\r\n')
        if len(data) == 1:
            data = str_csv.split('\n')
        new_data = []
        element_count = -1
        for row in data:
            lst = row.split(',')
            if element_count == -1:
                element_count = len(lst)
            if len(lst) == element_count:
                new_data.append(row)
        data = new_data
        str_csv = '\n'.join(data)
        # make StringIO
        f = StringIO.StringIO(str_csv)
        # make csv reader
        reader = csv.reader(f, delimiter = ',')
        lst = []
        element_count = -1
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
        import numpy as np
        data_list = self.csv_to_list(csv)
        if caption_list is None:
            caption_list = data_list[0]
            data_list = data_list[1:]
        elif data_list[0] == caption_list:
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
                row.append(0.0)
            data.append(row[:-1])
            target.append(row[-1])
        data = np.array(data)
        target = np.array(target)
        return (data, target, caption_list, numeric_value)

    def action_result(self):
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
        if 'draw_plot' in request.POST and request.POST['draw_plot'] == 'true':
            draw_plot = True
        else:
            draw_plot = False

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
                del prediction_target
            else:
                do_prediction = False
                predict_csv = ''
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

        # Available classes (we call it as groups, since class is reserved word in Python)
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
        subplot_num *= 2
        if subplot_num == 1:
            row_count = 1
            col_count = 1
        else:
            row_count = np.ceil(subplot_num / 2)
            col_count = 2
        # make figure
        plot_url = ''
        if draw_plot:
            try:
                fig = plt.figure(figsize=(6.0*col_count, 6.0*row_count))
                fig.subplots_adjust(hspace = 0.2, wspace = 0.2)
                fig.suptitle('Dimension Projection')
                # subplot
                subplot_index = 1
                for mode in xrange(2):
                    if mode == 0:
                        data = training_data
                        target = training_target
                        caption = 'training'
                    else:
                        data = testing_data
                        target = testing_target
                        caption = 'testing'
                    second_dimension_start_index = 1
                    first_dimension_index = 0
                    for first_dimension in dimensions:
                        second_dimension_index = second_dimension_start_index
                        x = data[:,first_dimension_index]
                        # determine x_min and x_max for contour
                        x_min, x_max = x.min(), x.max()
                        x_range = x_max - x_min
                        x_max += 0.1 * x_range
                        x_min -= 0.1 * x_range
                        for second_dimension in dimensions[second_dimension_start_index:]:
                            ax = fig.add_subplot(row_count, col_count, subplot_index)
                            y = data[:,second_dimension_index]
                            y_min, y_max = y.min(), y.max()
                            y_range = y_max - y_min
                            y_max += 0.1 * y_range
                            y_min -= 0.1 * y_range
                            # xx, yy
                            xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01 * x_range),
                                 np.arange(y_min, y_max, 0.01 * y_range))
                            tup = ()
                            for i in xrange(len(data[0])):
                                if i == first_dimension_index:
                                    tup = tup + ( xx.ravel(), )
                                elif i == second_dimension_index:
                                    tup = tup + ( yy.ravel(), )
                                else:
                                    dimension_mean = data[:, i].mean()
                                    tup = tup + ([dimension_mean] * len(xx.ravel()) , )
                            Z = classifier.predict(np.c_[tup])
                            Z = Z.reshape(xx.shape)
                            ax.contourf(xx, yy, Z)
                            # scatter-plot the data
                            ax.scatter(x, y, c=target, cmap=plt.cm.gist_rainbow)
                            ax.set_title (first_dimension + ' vs ' + second_dimension + ' ('+caption+')')
                            ax.set_xlabel(first_dimension)
                            ax.set_ylabel(second_dimension)
                            subplot_index += 1
                            second_dimension_index += 1
                        first_dimension_index += 1
                        second_dimension_start_index += 1
                # make canvas
                file_name = 'classification/plot_'+str(np.random.randint(10000))+str(time.time())+'.png'
                plot_url = draw_matplotlib_figure(fig,file_name,'example')
            except Exception, e:
                result['success'] = False
                result['message'] = 'Unexpected error while creating plot : '+ e.message
            if not result['success']:
                return json.dumps(result)

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
        prediction_data = self.csv_to_list(predict_csv)
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
                  'plot_url'              : plot_url,
                  'draw_plot'             : draw_plot,
                  'dimensions'            : dimensions
            }
        return json.dumps(result)
