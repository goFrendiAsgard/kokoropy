from kokoropy import load_view, base_url, request, publish_methods, load_template, \
    application_path, file_get_contents
from sqlalchemy.ext.declarative import declared_attr
import math, random, os, json, sys
from model import DB_Model
from operator import and_, or_
from kokoropy import var_dump

class Multi_Language_Controller(object):
    
    def preprocess_content(self, content):
        return content
    
    def load_view(self, application_name, view_name, *args, **kwargs):
        # get content
        content = load_view(application_name, view_name, *args, **kwargs)
        # preprocess
        return self.preprocess_content(content)

class Crud_Controller(Multi_Language_Controller):
    __model__       = None
    __base_view__   = None
    
    def search_input(self):
        return self._load_view('search')
    
    def default_criterion(self):
        return self.__model__._real_id > 0
    
    def search_criterion(self):
        q = request.GET['__q'] if '__q' in request.GET else None
        criterion = self.__model__._real_id > 0
        if self.__model__ is not None and q is not None:
            q_parts = q.replace('-',' ').replace('_',' ').replace('/',' ').split(' ')
            model_obj = self.__model__()
            column_names = model_obj._column_list
            for q in q_parts:
                tmp_criterion = self.__model__._real_id < 0 # False
                for column_name in column_names:
                    prop = getattr(self.__model__, column_name)
                    if column_name in model_obj._get_relation_names():
                        ref_metadata = model_obj._get_relation_metadata(column_name)
                        ref_class = model_obj._get_relation_class(column_name)
                        ref_obj = ref_class()
                        sub_column_names = ref_obj._column_list
                        for sub_column_name in sub_column_names:
                            # only applied to actual column
                            if sub_column_name in ref_obj._get_actual_column_names():
                                sub_column = getattr(ref_class, sub_column_name)
                                if ref_metadata.uselist:
                                    # one to many
                                    tmp_criterion = or_(tmp_criterion, prop.any(sub_column.ilike(q + '%')))
                                    tmp_criterion = or_(tmp_criterion, prop.any(sub_column.ilike('% '+q+'%')))
                                    tmp_criterion = or_(tmp_criterion, prop.any(sub_column.ilike('%-'+q+'%')))
                                    tmp_criterion = or_(tmp_criterion, prop.any(sub_column.ilike('%/'+q+'%')))
                                    tmp_criterion = or_(tmp_criterion, prop.any(sub_column.ilike('%|_'+q+'%', escape='|')))
                                else:
                                    # many to one
                                    tmp_criterion = or_(tmp_criterion, prop.has(sub_column.ilike(q + '%')))
                                    tmp_criterion = or_(tmp_criterion, prop.has(sub_column.ilike('% '+q+'%')))
                                    tmp_criterion = or_(tmp_criterion, prop.has(sub_column.ilike('%-'+q+'%')))
                                    tmp_criterion = or_(tmp_criterion, prop.has(sub_column.ilike('%/'+q+'%')))
                                    tmp_criterion = or_(tmp_criterion, prop.has(sub_column.ilike('%|_'+q+'%', escape='|')))
                    elif column_name in model_obj._get_actual_column_names():
                        tmp_criterion = or_(tmp_criterion, prop.ilike(q + '%'))
                        tmp_criterion = or_(tmp_criterion, prop.ilike('% '+q+'%'))
                        tmp_criterion = or_(tmp_criterion, prop.ilike('%-'+q+'%'))
                        tmp_criterion = or_(tmp_criterion, prop.ilike('%/'+q+'%'))
                        tmp_criterion = or_(tmp_criterion, prop.ilike('%|_'+q+'%', escape='|'))
                criterion = and_(criterion, tmp_criterion)
        return criterion
    
    @declared_attr
    def __application_name__(self):
        path = sys.modules[self.__module__].__file__
        return os.path.dirname(os.path.dirname(path)).split('/')[-1]
    
    @declared_attr
    def __url_list__(self):
        view_list = ['list', 'show', 'new', 'create', 'edit', 'update', 'trash', 'untrash', 'remove', 'delete', 'destroy']
        url = base_url(self.__application_name__+'/' + self.__model_name__) + '/'
        url_list = {'index' : url}
        for view in view_list:
            url_list[view] = url + view
        return url_list
    
    @declared_attr
    def __view_directory__(self):
        if self.__model__ is not None:
            return self.__model__.__name__.lower()
        return ''
    
    @declared_attr
    def __model_name__(self):
        if self.__model__ is not None:
            return self.__model__.__name__.lower()
        return ''
    
    @declared_attr
    def __caption__(self):
        if hasattr(self.__model__, '__caption__'):
            return self.__model__.__caption__
        return ''
    
    @declared_attr
    def __row_per_page__(self):
        return 5;
    
    @classmethod
    def publish_route(cls):
        obj = cls()
        obj._fill_url_list()
        method_names = cls.__url_list__.keys()
        methods = []
        for method_name in method_names:
            methods.append((method_name, getattr(obj, method_name)))
        publish_methods(cls.__application_name__, cls.__model_name__, methods)
    
    def _fill_url_list(self):
        view_list = ['list', 'show', 'new', 'create', 'edit', 'update', 'trash', 'remove', 'delete', 'destroy']
        url = base_url(self.__application_name__+'/' + self.__model_name__) + '/'
        for view in view_list:
            if view not in self.__url_list__:
                self.__url_list__[view] = url + view
    
    def _setup_view_parameter(self):
        self._fill_url_list()
        self._view_parameter = {
                'url_list'      : self.__url_list__,
                'caption'       : self.__caption__,
                'base_view'     : self.__base_view__
            }
    
    def _set_view_parameter(self, key, value):
        if not hasattr(self, '_view_parameter'):
            self._setup_view_parameter()
        self._view_parameter[key] = value
    
    def _get_view_parameter(self, key = None):
        if not hasattr(self, '_view_parameter'):
            self._setup_view_parameter()
        if key is None:
            return self._view_parameter
        elif key in self._view_parameter:
            return self._view_parameter[key]
    
    def _get_view_parameter_as_json(self, key = None):
        # change everything to isoformat to prevent error
        dct = {}
        for key in self._get_view_parameter(key):
            value = self._get_view_parameter(key)
            if isinstance(value, DB_Model):
                value = value.to_dict(isoformat = True)
            elif isinstance(value, list):
                new_value = []
                for item in value:
                    if isinstance(item, DB_Model):
                        item = item.to_dict(isoformat = True)
                    elif hasattr(value, 'isoformat'):
                        item = item.isoformat()
                    new_value.append(item)
                value = new_value
            elif hasattr(value, 'isoformat'):
                value = value.isoformat()
            dct[key] = value
        # message should be translated
        if 'message' in dct:
            dct['message'] = self.preprocess_content(dct['message'])
        return json.dumps(dct)
    
    def _load_view(self, view):
        if os.path.exists(application_path(os.path.join(self.__application_name__, 'views', self.__model_name__, view))):
            # normal load_view (if view exists)
            content = load_view(self.__application_name__, self.__model_name__ + '/' + view, **self._get_view_parameter())
        else:
            # take default key content
            content = ''
            content = file_get_contents(os.path.join(os.path.dirname(__file__), 'views', view + '.html'))
            content = content.replace('G_Table_Name', self.__model_name__.title())
            content = content.replace('g_table_name', self.__model_name__)
            content = content.replace('g_application_name', self.__application_name__)
            # do load_template
            content = load_template(content, **self._get_view_parameter())
        return self.preprocess_content(content)
    
    def load_view(self, application_name, view_name, *args, **kwargs):
        # add some default view parameter to kwargs
        if not hasattr(self, '_view_parameter'):
            self._setup_view_parameter()
        for key in self._view_parameter:
            if key not in kwargs:
                kwargs[key] = self._get_view_parameter(key)
        # call Multi_Language_Controller's load_view
        content = Multi_Language_Controller.load_view(self, application_name, view_name, *args, **kwargs)
        return content
    
    def _token_key(self):
        return '__token_' + self.__application_name__ + '_' + self.__model_name__
    
    def _set_token(self):
        new_token = str.zfill(str(random.randrange(0,10000)), 5)
        tokens =self._get_token()
        tokens.append(new_token)
        request.SESSION[self._token_key()] = ','.join(tokens)
        return new_token
    
    def _get_token(self):
        if self._token_key() not in request.SESSION:
            request.SESSION[self._token_key()] = ''
        return request.SESSION[self._token_key()].split(',')
    
    def _is_token_match(self, token):
        tokens = self._get_token()
        match = token in tokens
        if match:
            tokens.remove(token)
            request.SESSION[self._token_key()] = ','.join(tokens)
        return match
    
    def index(self):
        return self.list()
    
    def list(self):
        ''' Show table '''
        # get page index
        current_page    = int(request.GET['page'] if 'page' in request.GET else 1)
        only_trashed    = True if 'trash' in request.GET and request.GET['trash'] == '1' else False
        # determine limit and offset
        limit   = self.__row_per_page__
        offset  = (current_page-1) * limit
        # get the data
        data_list = self.__model__.get(and_(self.default_criterion(), self.search_criterion()), limit = limit, offset = offset, only_trashed = only_trashed)
        for data in data_list:
            data.set_state_list()
        # calculate page count
        page_count = int(math.ceil(float(self.__model__.count(and_(self.default_criterion(), self.search_criterion()))/float(limit))))
        # serialized get
        get_pair = []
        for key in request.GET:
            if key == 'page' or request.GET[key] == '':
                continue
            get_pair.append(key + '=' + str(request.GET[key]))
        get_pair = '&'.join(get_pair)
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__+'_list', data_list)
        self._set_view_parameter(self.__model_name__.title(), self.__model__)
        self._set_view_parameter('__token', self._set_token())
        self._set_view_parameter('current_page', current_page)
        self._set_view_parameter('page_count', page_count)
        self._set_view_parameter('search_input', self.search_input())
        self._set_view_parameter('serialized_get', get_pair)
        self._set_view_parameter('only_trashed', only_trashed)
        return self._load_view('list')
    
    def show(self, id=None):
        ''' Show One Record '''
        data = self.__model__.find(id, include_trashed = True)
        if data is not None:
            data.set_state_show()
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        return self._load_view('show')
    
    def new(self):
        ''' Insert Form '''
        data = self.__model__()
        data.set_state_insert()
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('__token', self._set_token())
        return self._load_view('new')
    
    def create(self):
        ''' Insert Action '''
        token = request.POST.pop('__token', '')
        if not self._is_token_match(token):
            success = False
            error_message = 'Invalid Token'
            data = None
        else:
            data = self.__model__()
            data.set_state_insert()
            # put your code here
            data.assign_from_dict(request.POST)
            data.save()
            # get result
            success = data.success
            error_message = data.error_message
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            if success:
                token = self._set_token()
            self._set_view_parameter('__token', token)
            return self._get_view_parameter_as_json()
        return self._load_view('create')
    
    def edit(self, id = None):
        ''' Update Form '''
        data = self.__model__.find(id)
        if data is not None:
            data.set_state_update()
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('__token', self._set_token())
        return self._load_view('edit')
    
    def update(self,id = None):
        ''' Update Action '''
        token = request.POST.pop('__token', '')
        if not self._is_token_match(token):
            success = False
            error_message = 'Invalid Token'
            data = None
        else:
            data = self.__model__.find(id)
            if data is not None:
                data.set_state_update()
                # put your code here
                data.assign_from_dict(request.POST)
                data.save()
                success = data.success
                error_message = data.error_message
            else:
                success = False
                error_message = 'Data Not Found'
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            if success:
                token = self._set_token()
            self._set_view_parameter('__token', token)
            return self._get_view_parameter_as_json()
        return self._load_view('update')
    
    def trash(self, id = None):
        ''' Trash Form '''
        data = self.__model__.find(id)
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('__token', self._set_token())
        return self._load_view('trash')
    
    def remove(self, id = None):
        ''' Trash Action '''
        token = request.POST.pop('__token', '')
        if not self._is_token_match(token):
            success = False
            error_message = 'Invalid Token'
            data = None
        else:
            data = self.__model__.find(id)
            if data is not None:
                data.trash()
                success = data.success
                error_message = data.error_message
            else:
                success = False
                error_message = 'Data Not Found'
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            if success:
                token = self._set_token()
            self._set_view_parameter('__token', token)
            return self._get_view_parameter_as_json()
        return self._load_view('remove')

    def untrash(self, id = None):
        token = request.POST.pop('__token', '')
        if not self._is_token_match(token):
            success = False
            error_message = 'Invalid Token'
            data = None
        else:
            data = self.__model__.find(id, True)
            if data is not None:
                data.untrash()
                success = data.success
                error_message = data.error_message
            else:
                success = False
                error_message = 'Data Not Found'
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            if success:
                token = self._set_token()
            self._set_view_parameter('__token', token)
            return self._get_view_parameter_as_json()
        return self._load_view('untrash')
    
    def delete(self, id=None):
        ''' Delete Form '''
        data = self.__model__.find(id, include_trashed = True)
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('__token', self._set_token())
        return self._load_view('delete')
    
    def destroy(self, id=None):
        ''' Delete Action '''
        token = request.POST.pop('__token', '')
        if not self._is_token_match(token):
            success = False
            error_message = 'Invalid Token'
            data = None
        else:
            data = self.__model__.find(id, include_trashed = True)
            if data is not None:
                data.delete()
                success = data.success
                error_message = data.error_message
            else:
                success = False
                error_message = 'Data Not Found'
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__model_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            if success:
                token = self._set_token()
            self._set_view_parameter('__token', token)
            return self._get_view_parameter_as_json()
        return self._load_view('destroy')