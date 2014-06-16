from kokoropy import load_view, base_url, request, publish_methods, load_template, \
    application_path, file_get_contents
from sqlalchemy.ext.declarative import declared_attr
import math, random, os, json
from model import Model
from operator import and_, or_
from kokoropy import var_dump
from sqlalchemy.sql.expression import BinaryExpression

class Multi_Language_Controller(object):
    
    def preprocess_content(self, content):
        return content
    
    def load_view(self, application_name, view_name, *args, **kwargs):
        # get content
        content = load_view(application_name, view_name, *args, **kwargs)
        # preprocess
        return self.preprocess_content(content)

class Crud_Controller(Multi_Language_Controller):
    __model__               = None
    __application_name__    = ''
    __view_directory__      = ''
    
    def search_input(self):
        q = request.GET['__q'] if '__q' in request.GET else ''
        html = '<input type="text" id="__q" name="__q" placeholder="Search" value="' + q + '" >'
        return html
    
    def default_criterion(self):
        q = request.GET['__q'] if '__q' in request.GET else None
        if self.__model__ is not None:
            model_obj = self.__model__()
            column_names = model_obj._column_list
            criterion = self.__model__._real_id < 0 # False
            for column_name in column_names:
                prop = getattr(self.__model__, column_name)
                if isinstance(property, Model):
                    pass
                else:
                    criterion = or_(criterion, prop.like(q))
        else:
            criterion = self.__model__._real_id > 0
        return criterion
    
    @declared_attr
    def __url_list__(self):
        view_list = ['list', 'show', 'new', 'create', 'edit', 'update', 'trash', 'remove', 'delete', 'destroy']
        url = base_url(self.__application_name__+'/' + self.__table_name__) + '/'
        url_list = {'index' : url}
        for view in view_list:
            url_list[view] = url + view
        return url_list
    
    @declared_attr
    def __table_name__(self):
        if hasattr(self.__model__, '__tablename__'):
            return self.__model__.__tablename__
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
        publish_methods(cls.__application_name__, cls.__table_name__, methods)
    
    def _fill_url_list(self):
        view_list = ['list', 'show', 'new', 'create', 'edit', 'update', 'trash', 'remove', 'delete', 'destroy']
        url = base_url(self.__application_name__+'/' + self.__table_name__) + '/'
        for view in view_list:
            if view not in self.__url_list__:
                self.__url_list__[view] = url + view
    
    def _setup_view_parameter(self):
        self._fill_url_list()
        self._view_parameter = {
                'url_list'      : self.__url_list__,
                'caption'       : self.__caption__
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
            if isinstance(value, Model):
                value = value.to_dict(isoformat = True)
            elif isinstance(value, list):
                new_value = []
                for item in value:
                    if isinstance(item, Model):
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
        if os.path.exists(application_path(os.path.join(self.__application_name__, 'views', self.__table_name__, view))):
            # normal load_view (if view exists)
            content = load_view(self.__application_name__, self.__table_name__ + '/' + view, **self._get_view_parameter())
        else:
            # take default key content
            content = ''
            content = file_get_contents(os.path.join(os.path.dirname(__file__), 'views', view + '.html'))
            content = content.replace('G_Table_Name', self.__table_name__.title())
            content = content.replace('g_table_name', self.__table_name__)
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
        return '__token_' + self.__application_name__ + '_' + self.__table_name__
    
    def _set_token(self):
        value = str.zfill(str(random.randrange(0,10000)), 5)
        request.SESSION[self._token_key()] = value
        return value
    
    def _is_token_match(self, token):
        value = request.SESSION.pop(self._token_key(), '')
        match = value == token
        self._set_token()
        return match
    
    def index(self):
        return self.list()
    
    def list(self):
        ''' Show table '''
        # get page index
        current_page = int(request.GET.pop('page', 1))
        # determine limit and offset
        limit = self.__row_per_page__
        offset = (current_page-1) * limit
        # get the data
        data_list = self.__model__.get(self.default_criterion(), limit = limit, offset = offset)
        # calculate page count
        page_count = int(math.ceil(float(self.__model__.count())/limit))
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__table_name__+'_list', data_list)
        self._set_view_parameter('current_page', current_page)
        self._set_view_parameter('page_count', page_count)
        self._set_view_parameter('search_input', self.search_input())
        return self._load_view('list')
    
    def show(self, id=None):
        ''' Show One Record '''
        data = self.__model__.find(id)
        if data is not None:
            data.set_state_show()
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__table_name__, data)
        return self._load_view('show')
    
    def new(self):
        ''' Insert Form '''
        data = self.__model__()
        data.set_state_insert()
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__table_name__, data)
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
        self._set_view_parameter(self.__table_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            self._set_view_parameter('__token', self._set_token())
            return self._get_view_parameter_as_json()
        return self._load_view('create')
    
    def edit(self, id = None):
        ''' Update Form '''
        data = self.__model__.find(id)
        if data is not None:
            data.set_state_update()
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__table_name__, data)
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
        self._set_view_parameter(self.__table_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            self._set_view_parameter('__token', self._set_token())
            return self._get_view_parameter_as_json()
        return self._load_view('update')
    
    def trash(self, id = None):
        ''' Trash Form '''
        data = self.__model__.find(id)
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__table_name__, data)
        self._set_view_parameter('__token', self._set_token())
        return self._load_view('show')
    
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
        self._set_view_parameter(self.__table_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            self._set_view_parameter('__token', self._set_token())
            return self._get_view_parameter_as_json()
        return self._load_view('remove')
    
    def delete(self, id=None):
        ''' Delete Form '''
        data = self.__model__.find(id)
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__table_name__, data)
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
            data = self.__model__.find(id)
            if data is not None:
                data.delete()
                success = data.success
                error_message = data.error_message
            else:
                success = False
                error_message = 'Data Not Found'
        # load the view
        self._setup_view_parameter()
        self._set_view_parameter(self.__table_name__, data)
        self._set_view_parameter('success', success)
        self._set_view_parameter('error_message', error_message)
        # if ajax request (or explicitly request response to be json)
        if request.is_xhr or request.POST.pop('__as_json', False):
            self._set_view_parameter('__token', self._set_token())
            return self._get_view_parameter_as_json()
        return self._load_view('destroy')