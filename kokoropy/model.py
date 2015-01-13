from sqlalchemy import or_, and_, ForeignKey, create_engine, func,\
    BIGINT, BigInteger, BINARY, Binary,\
    BOOLEAN, Boolean, DATE, Date, DATETIME, DateTime, FLOAT, Float,\
    INTEGER, Integer, VARCHAR, String, TEXT, Text, MetaData, util
from sqlalchemy import Column as SA_Column
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref, validates
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.types import TypeDecorator, Unicode, UnicodeText
from alembic.migration import MigrationContext
from alembic.operations import Operations
from kokoropy import Fore, Back, base_url, request, save_uploaded_asset, var_dump, decode_string, encode_string
from kokoropy import html as HTML
import datetime, time, json, sys, os, asset

# initialize logger
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create Base
Base = declarative_base()

if sys.version_info >= (3,0,0):
    xrange = range

def creator_maker(class_name, relation_name):
    '''
    return lambda function for association_proxy's creator parameter
    '''
    return eval('lambda _val: ' + class_name + '(' + relation_name + ' = _val)')

def fk_column(fk, **kwargs):
    '''
    usage:
        fk_column('theme._real_id')
    or:
        fk_column('theme._real_id', unique = False, nullable = True)
    is a shortcut for
        Column(Integer, ForeignKey('theme._real_id), index = True, unique = False, nullable = True)
    '''
    return SA_Column(Integer, ForeignKey(fk), **kwargs)

def _rel(*args, **kwargs):
    args = list(args)
    fk = args.pop()
    if len(args) == 0:
        class_name = '.'.join(fk.split('.')[0:-1])
    else:
        class_name = args.pop()
    args.insert(0, class_name)
    args = tuple(args)
    kwargs['foreign_keys'] = fk
    return relationship(*args, **kwargs)

def one_to_many(*args, **kwargs):
    '''
    usage:
        one_to_many('Page', 'Page_Group.fk_page')
        one_to_many('Page_Group.fk_page')
    is a shortcut to:
        relationship('Page_Group', foreign_keys='Page_Group.fk_page', uselist = True)
    '''
    kwargs['uselist'] = True
    return _rel(*args, **kwargs)

def many_to_one(*args, **kwargs):
    '''
    usage:
        many_to_one('Theme', 'Page.fk_theme')
    is a shortcut to:
        relationship("Theme", foreign_keys="Page.fk_theme", uselist = False)
    '''
    kwargs['uselist'] = False
    return _rel(*args, **kwargs)

def lookup_proxy(*args, **kwargs):
    '''
    usage:
        lookup_proxy('page_groups', lookup='Page_Group.group')
    or:
        lookup_proxy('page_groups', 'Page_Group.group')
    is a shortcut to
        lookup_proxy('page_groups', 'group', creator = lambda _val: Page_Group(group = _val))

    example:

    class Page(DB_Model):
        __session__ = session
        page_groups = relationship("Page_Group", foreign_keys="Page_Group.fk_page")
        groups      = lookup_proxy(page_groups, lookup='Page_Group.group')

    class Page_Group(DB_Model):
        __session__ = session
        fk_page     = Column(Integer, ForeignKey("page._real_id"))
        fk_group    = Column(Integer, ForeignKey("group._real_id"))
        page        = relationship("Page", foreign_keys="Page_Groups.fk_page")
        group       = relationship("Group", foreign_keys="Page_Groups.fk_group")

    class Group(DB_Model):
        __session__ = session
        name        = Column(String(20))
    '''
    args = list(args)
    if 'lookup' in kwargs:
        lookup = kwargs.pop("lookup",'')
    elif len(args) > 1:
        lookup = args.pop() 
    else:
        lookup = ''   
    lookup_part = lookup.split('.')
    relation_name = lookup_part[-1]
    class_name = '.'.join(lookup_part[0:-1])
    kwargs['creator'] = creator_maker(class_name, relation_name)    
    if len(args) == 1:
        args.append(relation_name)
    return association_proxy(*args, **kwargs)

class Resource(object):
    '''
    usage:
        x = Resource()
        x += 'var y = 5;'
        x.append('javascript.js')
        print x.compiled
    output:
        <script type="text/javascript">var y = 5;</script>
        <script type="text/javascript" src="javascript.js"></script>
    '''
    def __init__(self):
        self._resource = []

    def append_internal(self, val):
        if ('internal', val) not in self._resource:
            self._resource.append(('internal', val))

    def append_external(self, val):
        if ('external', val) not in self._resource:
            self._resource.append(('external', val))

    def append_compiled(self, val):
        if ('compiled', val) not in self._resource:
            self._resource.append(('compiled', val))

    def __add__(self, val):
        if isinstance(val, Resource):
            for res in val._resource:
                if res not in self._resource:
                    self._resource.append(res)
        else:
            self.append_internal(val)
        return self

    def append(self, val):
        self.append_external(val)

    def compile_external_resource(self, res):
        return '<script type="text/javascript" src="' + res + '"></script>'

    def compile_internal_resource(self, res):
        return '<script type="text/javascript">' + res + '</script>'

    @property
    def compiled(self):
        compilation = ''
        for (type_,res) in self._resource:
            if res is None:
                continue
            res = str(res)
            if type_ == 'external':
                compilation += self.compile_external_resource(res)
            elif type_ == 'internal':
                compilation += self.compile_internal_resource(res)
            else:
                compilation += res
        return compilation

class JS_Resource(Resource):
    pass

class CSS_Resource(Resource):
    def compile_external_resource(self, res):
        return '<link rel="stylesheet" type="text/css" href="' + res + '">'

    def compile_internal_resource(self, res):
        return '<style type="text/css">' + res + '</style>'


class BaseConfig(object):
    '''
    BaseConfig class, should be inherited in model's _config to ensure there are just
    one engine, session, and metadata across models
    '''
    __property = {}

    def __init__( self, connection_string, *args, **kwargs):
        engine = create_engine(connection_string, *args, **kwargs)
        engine.raw_connection().connection.text_factory = str
        session = scoped_session(sessionmaker(bind=self.engine))
        metadata = MetaData()
        metadata.bind = engine
        self.set_property('engine', engine)
        self.set_property('session', session)
        self.set_property('metadata', metadata)

    @property
    def engine(self):
        return self.get_property('engine')

    @property
    def session(self):
        return self.get_property('session')

    @property
    def metadata(self):
        return self.get_property('metadata')

    @declared_attr
    def application_name(self):
        path = sys.modules[self.__module__].__file__
        return os.path.dirname(os.path.dirname(path)).split('/')[-1]
    
    def set_property(self, key, value):
        key = self.application_name + key
        if key not in BaseConfig.__property:
            BaseConfig.__property[key] = value
    
    def get_property(self, key):
        key = self.application_name + key
        if key in BaseConfig.__property:
            return BaseConfig.__property[key]

# override sqlAlchemy's Column class, add coltype property
class Column(SA_Column):
    def __init__(self, *args, **kwargs):
        args_type = None
        kwargs_type = None
        # get type from kwargs
        if 'type_' in kwargs:
            kwargs_type = kwargs['type_']
        # get type from args
        args = list(args)
        if args:
            if len(args) > 0:
                if isinstance(args[0], util.string_types) and len(args) > 1:
                    args_type = args[1]
                else:
                    args_type = args[0]
        # set coltype
        if kwargs_type is not None:
            coltype = kwargs_type
        else:
            coltype = args_type
        # save the coltype so that it can be fetched later
        self._coltype = coltype
        super(Column, self).__init__(*args, **kwargs)

    def is_coltype_match(self, cls):
        return isinstance(self._coltype, cls) or self._coltype == cls

    def get_coltype_attr(self, attr):
        if hasattr(self._coltype, attr):
            return getattr(self._coltype, attr)
        else:
            return None

    def is_coltype_attr_match(self, attr, value):
        if not hasattr(self._coltype, attr):
            return False
        attr = getattr(self._coltype, attr)
        return attr == value

class Password(TypeDecorator):
    impl = Unicode

class Upload(TypeDecorator):
    impl = Unicode
    def __init__(self, *args, **kwargs):
        self.is_image = kwargs.pop('is_image', False)
        super(Upload, self).__init__(*args, **kwargs)

class Option(TypeDecorator):
    impl = Unicode
    def __init__(self, *args, **kwargs):
        # take options parameter
        self.options = kwargs.pop('options',{})
        if isinstance(self.options, list):
            new_options = {}
            for option in self.options:
                new_options[option] = option
            self.options = new_options
        self.multiple = kwargs.pop('multiple', False)
        super(Option, self).__init__(*args, **kwargs)

class RichText(TypeDecorator):
    impl = UnicodeText

class Code(TypeDecorator):
    impl = UnicodeText
    def __init__(self, *args, **kwargs):
        self.theme = kwargs.pop('theme', 'monokai')
        self.language = kwargs.pop('language', 'python')
        super(Code, self).__init__(*args, **kwargs)


def _db_operation_method(func):
    '''
    Decorator for DB_Model's method that use session. add try-except automatically
    '''
    def func_wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception, e:
            self.session.rollback()
            logger.error('Database commit failed, ' + str(e))
            self.success = False
            self.error_message = str(e)
    return func_wrapper

def _static_db_operation_method(func):
    '''
    Decorator for DB_Model's static method that use session. Add try-except automatically
    '''
    def func_wrapper(cls, *args, **kwargs):
        if hasattr(cls,'__session__ '):
            session = cls.__session__
        else:
            obj = cls()
            session = obj.session
        try:
            return func(cls, *args, **kwargs)
        except Exception, e:
            session.rollback()
            raise
    return func_wrapper

        
class DB_Model(Base):
    '''
    DB_Model
    '''
    # defaults
    _real_id        = Column(Integer, primary_key=True)
    _trashed        = Column(Boolean, default=False)
    _created_at     = Column(DateTime, default=func.now())
    _updated_at     = Column(DateTime, default=func.now(), onupdate=func.now())
    id              = Column(String(35), unique=True)
    # state
    __state__               = None # show, insert, update, delete
    # configurations
    __abstract__            = True
    __connection_string__   = ''
    __echo__                = True
    __id_prefix__           = '%Y%m%d-'
    __id_digit__     = 5
    # columns to be shown
    __shown_column__                    = None
    __form_column__                     = None
    __insert_column__                   = None
    __update_column__                   = None
    __virtual_shown_column__            = None
    __virtual_form_column__             = None
    __virtual_insert_column__           = None
    __virtual_update_column__           = None
    __excluded_shown_column__           = None
    __excluded_form_column__            = None
    __excluded_insert_column__          = None
    __excluded_update_column__          = None
    # columns to be shown on tabular
    __tabular_shown_column__            = None
    __tabular_form_column__             = None
    __tabular_insert_column__           = None
    __tabular_update_column__           = None
    __tabular_virtual_shown_column__    = None
    __tabular_virtual_form_column__     = None
    __tabular_virtual_insert_column__   = None
    __tabular_virtual_update_column__   = None
    __tabular_excluded_shown_column__   = None
    __tabular_excluded_form_column__    = None
    __tabular_excluded_insert_column__  = None
    __tabular_excluded_update_column__  = None
    # columns to be shown on one to many
    __detail_shown_column__             = {}
    __detail_form_column__              = {}
    __detail_insert_column__            = {}
    __detail_update_column__            = {}
    __detail_virtual_shown_column__     = {}
    __detail_virtual_form_column__      = {}
    __detail_virtual_insert_column__    = {}
    __detail_virtual_update_column__    = {}
    __detail_excluded_shown_column__    = {}
    __detail_excluded_form_column__     = {}
    __detail_excluded_insert_column__   = {}
    __detail_excluded_update_column__   = {}
    # label
    __column_label__                    = {}
    __detail_column_label__             = {}
    # automatic assigned columns (when read data from controller)
    __automatic_assigned_column__        = None
    __automatic_assigned_insert_column__ = None
    __automatic_assigned_update_column__ = None
    # privilege
    __allow_list__      = True
    __allow_show__      = True
    __allow_edit__      = True
    __allow_new__       = True
    __allow_trash__     = True
    __allow_untrash__   = True
    __allow_delete__    = True
    
    @declared_attr
    def __tablename__(self):
        # self is refered to class, not "this"
        return self.__name__.lower()
    
    @declared_attr
    def __caption__(self):
        table_name = self.__tablename__
        return table_name.replace('_', ' ').title()
    
    @declared_attr
    def __application_name__(self):
        path = sys.modules[self.__module__].__file__
        return os.path.dirname(os.path.dirname(path)).split('/')[-1]
    
    @property
    def state(self):
        if self.__state__ is None:
            if self._real_id is None:
                self.__state__ = 'insert'
            else:
                self.__state__ = 'update'
        return self.__state__
    
        
    def _set_state(self, state):
        self.__state__ = state

    def set_state_list(self):
        self._set_state('list')
    
    def set_state_show(self):
        self._set_state('show')
    
    def set_state_insert(self):
        self._set_state('insert')
    
    def set_state_update(self):
        self._set_state('update')
    
    def set_state_delete(self):
        self._set_state('delete')
    
    def is_list_state(self):
        return self.state == 'list'
    
    def is_show_state(self):
        return self.state == 'show'
    
    def is_insert_state(self):
        return self.state == 'insert'
    
    def is_update_state(self):
        return self.state == 'update'
    
    def is_delete_staet(self):
        return self.state == 'delete'
    
    @property
    def _column_list(self):
        column_list             = []
        excluded_column_list    = []
        virtual_column_list     = []
        state = self.state
        # set priorities
        column_list_priorities          = []
        excluded_column_list_priorities = []
        virtual_column_list_priorities  = []
        if state == 'insert':
            column_list_priorities          = [self.__insert_column__, self.__form_column__, self.__shown_column__]
            excluded_column_list_priorities = [self.__excluded_insert_column__, self.__excluded_form_column__]
            virtual_column_list_priorities  = [self.__virtual_insert_column__, self.__virtual_form_column__]
        elif state == 'update':
            column_list_priorities          = [self.__update_column__, self.__form_column__, self.__shown_column__]
            excluded_column_list_priorities = [self.__excluded_update_column__, self.__excluded_form_column__]
            virtual_column_list_priorities  = [self.__virtual_update_column__, self.__virtual_form_column__]
        else:
            column_list_priorities          = [self.__shown_column__]
            excluded_column_list_priorities = [self.__excluded_shown_column__]
            virtual_column_list_priorities  = [self.__virtual_shown_column__]
        # assign default value to column_list
        for config_list in column_list_priorities:
            if config_list is not None:
                column_list = config_list
                break
        if len(column_list) == 0:
            column_list = self._get_actual_column_names() + self._get_relation_names()
            new_column_list = []
            for column_name in column_list:
                if column_name[:1] == '_' or column_name[:3] == 'fk_':
                    continue
                new_column_list.append(column_name)
            column_list = new_column_list
        # add virtual_columns
        for config_list in virtual_column_list_priorities:
            if config_list is not None:
                virtual_column_list = config_list
                break
        column_list += virtual_column_list
        # remove excluded_columns
        for config_list in excluded_column_list_priorities:
            if config_list is not None:
                excluded_column_list = config_list
                break
        for column_name in excluded_column_list:
            if column_name in column_list:
                column_list.remove(column_name)
        return column_list
    
    @property
    def _tabular_column_list(self):
        column_list          = []
        excluded_column_list = []
        virtual_column_list  = []
        state = self.state
        # set priorities
        column_list_priorities          = []
        excluded_column_list_priorities = []
        virtual_column_list_priorities  = []
        if state == 'insert':
            column_list_priorities          = [self.__tabular_insert_column__, self.__tabular_form_column__, self.__tabular_shown_column__]
            excluded_column_list_priorities = [self.__tabular_excluded_insert_column__, self.__tabular_excluded_form_column__]
            virtual_column_list_priorities  = [self.__tabular_virtual_insert_column__, self.__tabular_virtual_form_column__]
        elif state == 'update':
            column_list_priorities          = [self.__tabular_update_column__, self.__tabular_form_column__, self.__tabular_shown_column__]
            excluded_column_list_priorities = [self.__tabular_excluded_update_column__, self.__tabular_excluded_form_column__]
            virtual_column_list_priorities  = [self.__tabular_virtual_update_column__, self.__tabular_virtual_form_column__]
        else:
            column_list_priorities          = [self.__tabular_shown_column__]
            excluded_column_list_priorities = [self.__tabular_excluded_shown_column__]
            virtual_column_list_priorities  = [self.__tabular_virtual_shown_column__]
        # assign default value to column_list
        for config_list in column_list_priorities:
            if config_list is not None:
                column_list = config_list
                break
        if len(column_list) == 0:
            column_list = self._column_list
        # add virtual_columns
        for config_list in virtual_column_list_priorities:
            if config_list is not None:
                virtual_column_list = config_list
                break
        column_list += virtual_column_list
        # remove excluded_columns
        for config_list in excluded_column_list_priorities:
            if config_list is not None:
                excluded_column_list = config_list
                break
        for column_name in excluded_column_list:
            if column_name in column_list:
                column_list.remove(column_name)
        return column_list
    
    def _get_detail_column_list(self, column_name):
        column_list = []
        excluded_column_list = []
        virtual_column_list = []
        state = self.state
        # set priorities
        column_list_priorities = []
        excluded_column_list_priorities = []
        virtual_column_list_priorities = []
        if state == 'insert':
            column_list_priorities = [self.__detail_insert_column__, self.__detail_form_column__, self.__detail_shown_column__]
            excluded_column_list_priorities = [self.__detail_excluded_insert_column__, self.__detail_excluded_form_column__]
            virtual_column_list_priorities = [self.__detail_virtual_insert_column__, self.__detail_virtual_form_column__]
        elif state == 'update':
            column_list_priorities = [self.__detail_update_column__, self.__detail_form_column__, self.__detail_shown_column__]
            excluded_column_list_priorities = [self.__detail_excluded_update_column__, self.__detail_excluded_form_column__]
            virtual_column_list_priorities = [self.__detail_virtual_update_column__, self.__detail_virtual_form_column__]
        else:
            column_list_priorities = [self.__detail_shown_column__]
            excluded_column_list_priorities = [self.__detail_excluded_shown_column__]
            virtual_column_list_priorities = [self.__detail_virtual_shown_column__]
        # assign default value to column_list
        for config_list in column_list_priorities:
            if column_name in config_list and len(config_list[column_name]) > 0:
                column_list = config_list[column_name]
                break
        if len(column_list) == 0:
            obj = self._get_relation_class(column_name)()
            obj._set_state(state)
            column_list = obj._tabular_column_list
            # remove id from detail column
            if 'id' in column_list and len(column_list)>1:
                column_list.remove('id')
        # add virtual_columns
        for config_list in virtual_column_list_priorities:
            if column_name in config_list and len(config_list[column_name]) > 0:
                virtual_column_list = config_list[column_name]
                break
        column_list += virtual_column_list
        # remove excluded_columns
        for config_list in excluded_column_list_priorities:
            if column_name in config_list and len(config_list[column_name]) > 0:
                excluded_column_list = config_list[column_name]
                break
        for item in excluded_column_list:
            if item in column_list:
                column_list.remove(item)
        return column_list
    
    @property
    def _assign_column_list(self):
        state = self.__state__
        column_list = []
        # insert or update
        if state == 'insert' and len(self.__automatic_assigned_insert_column__) > 0:
            column_list = self.__automatic_assigned_insert_column__
        elif state == 'update' and len(self.__automatic_assigned_update_column__) > 0:
            column_list = self.__automatic_assigned_update_column__
        # show
        if len(self.__automatic_assigned_column__) > 0:
            column_list = self.__automatic_assigned_column__
        if len(column_list) == 0:
            column_list = self._get_actual_column_names() + self._get_relation_names()
        return column_list
    
    @property
    def _automatic_assigned_column(self):
        if self.__automatic_assigned_column__ is not None:
            automatic_assigned_column = self.__automatic_assigned_column__
        else:
            automatic_assigned_column = self._column_list
        return automatic_assigned_column
    
    @property
    def engine(self):
        if hasattr(self, '__session__'):
            self.__engine__ = self.session.bind
        elif not hasattr(self, '__engine__'):
            self.__engine__ = create_engine(self.__connection_string__, echo=self.__echo__)
        return self.__engine__
    
    @property
    def session(self):
        if not hasattr(self, '__session__'):
            if not hasattr(self, '__engine__'):
                self.__engine__ = create_engine(self.__connection_string__, echo=self.__echo__)
            self.__session__ = scoped_session(sessionmaker(bind=self.__engine__))
        return self.__session__
    
    @property
    def error_message(self):
        if hasattr(self, '_error_message'):
            return self._error_message
        else:
            return ''
    
    @error_message.setter
    def error_message(self, val):
        self._error_message = val
    
    @property
    def generated_html(self):
        if hasattr(self, '_generated_html'):
            return self._generated_html
        else:
            return ''
    
    @generated_html.setter
    def generated_html(self, val):
        self._generated_html = val
    
    @property
    def generated_css(self):
        if hasattr(self, '_generated_css'):
            return self._generated_css
        else:
            return CSS_Resource()
    
    @generated_css.setter
    def generated_css(self, val):
        self._generated_css = val
    
    @property
    def generated_js(self):
        if hasattr(self, '_generated_js'):
            return self._generated_js
        else:
            return JS_Resource()
    
    @generated_js.setter
    def generated_js(self, val):
        self._generated_js = val
    
    @property
    def success(self):
        if hasattr(self, '_success'):
            return self._success
        else:
            return True
    
    @success.setter
    def success(self, val):
        self._success = val

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    @property
    def trashed(self):
        return self._trashed
    
    @classmethod
    @_static_db_operation_method
    def get(cls, *criterion, **kwargs):
        '''
        Usage:
            DB_Model.get(DB_Model.name=="whatever", limit=1000, offset=0, include_trashed=True, as_json=True, include_relation=True)
        '''
        # get kwargs parameters
        limit               = kwargs.pop('limit', 1000)
        offset              = kwargs.pop('offset', 0)
        only_trashed        = kwargs.pop('only_trashed', False)
        include_trashed     = kwargs.pop('include_trashed', False)
        as_json             = kwargs.pop('as_json', False)
        include_relation    = kwargs.pop('include_relation', False)
        order_by            = kwargs.pop('order_by', None)
        # get / make session if not exists
        if hasattr(cls,'__session__ '):
            session = cls.__session__
        else:
            obj = cls()
            session = obj.session

        query = session.query(cls)
        # define "where" for trashed
        if only_trashed == True:
            query = query.filter(cls._trashed == True)
        else:
            if include_trashed == False:
                query = query.filter(cls._trashed == False)
        # run the query
        if order_by is None:
            result = query.filter(*criterion).limit(limit).offset(offset).all()
        else:
            result = query.filter(*criterion).order_by(order_by).limit(limit).offset(offset).all()

        # as json
        if as_json:
            kwargs = {'include_relation' : include_relation, 'isoformat' : True}
            result_list = []
            for row in result:
                result_list.append(row.to_dict(**kwargs))
            return json.dumps(result_list)
        else:
            return result
    
    @classmethod
    @_static_db_operation_method
    def count(cls, *criterion, **kwargs):
        # get kwargs parameters
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)
        include_trashed = kwargs.pop('include_trashed', False)
        # get / make session if not exists
        if hasattr(cls,'__session__ '):
            session = cls.__session__
        else:
            obj = cls()
            session = obj.session
        # count
        query = session.query(cls)
        if include_trashed == False:
            query = query.filter(cls._trashed == False)
        # apply filter
        query = query.filter(*criterion)
        # apply limit & offset
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.count()
        
    @classmethod
    def find(cls, id_value, include_trashed = False):
        result = cls.get(cls.id == id_value, include_trashed = include_trashed)
        if len(result)>0:
            row =  result[0]
        else:
            return None
        # sort the relation
        for relation_name in row._get_relation_names():
            relation_class = row._get_relation_class(relation_name)
            if issubclass(relation_class, Ordered_DB_Model):
                relation = getattr(row, relation_name)
                relation = sorted(relation, key = lambda x : x._index)
                setattr(row, relation_name, relation)
        return row
    
    def assign_from_dict(self, variable):
        for column_name in self._automatic_assigned_column:
            if column_name in self._get_actual_column_names():
                column_type = self._get_actual_column_type(column_name)
                if column_name in variable and variable[column_name] != '':
                    value = variable[column_name]
                    if self.is_coltype_match(column_name, Upload): # upload
                        value = value.filename if hasattr(value,'filename') else None
                    elif isinstance(column_type, Date): # date
                        if value != '' and value is not None:
                            y,m,d = value.split('-')
                            y,m,d  = int(y), int(m), int(d)
                            value = datetime.date(y,m,d)
                        else:
                            value = None
                    elif isinstance(column_type, DateTime): # datetime
                        if value != '' and value is not None:
                            date_part, time_part = value.split(' ')
                            y,m,d = date_part.split('-')
                            h,i,s = time_part.split(':')
                            y,m,d = int(y), int(m), int(d)
                            h,i,s = int(h), int(i), int(s)
                            value = datetime.datetime(y,m,d,h,i,s)
                        else:
                            value = None
                    elif isinstance(column_type, Boolean):
                        if value == '0':
                            value = False
                        else:
                            value = True
                    if value is not None:
                        value = decode_string(value)
                        setattr(self, column_name, value)
            elif column_name in self._get_relation_names():
                relation_metadata = self._get_relation_metadata(column_name)
                # one to many
                if relation_metadata.uselist:
                    ref_class = self._get_relation_class(column_name)

                    ref_obj = ref_class()
                    # determine if the model is ordered
                    is_ordered = isinstance(ref_obj, Ordered_DB_Model)
                    # custom_label and shown column
                    custom_label = self.__detail_column_label__[column_name]\
                        if column_name in self.__detail_column_label__ else {}
                    shown_column = self._get_detail_column_list(column_name)

                    # if only one column to be shown and it is a relationship
                    if len(shown_column) == 1 and shown_column[0] in ref_obj._get_relation_names():
                        list_val       = [] # value from variable
                        list_lookup    = [] # lookup (from list_val)
                        list_old       = [] # old lookup value (from database)
                        relation_value = [] # old relation value (from database)
                        lookup_class   = ref_obj._get_relation_class(shown_column[0])
                        # get list value
                        variable_key = column_name + '[]'
                        if hasattr(variable, 'getall') and variable_key in variable:                            
                            list_val = variable.getall(variable_key)
                        # get list_lookup based on list_val                        
                        for val in list_val:
                            list_lookup.append(lookup_class.find(val))
                        # get old relation_value
                        relation_value = self._get_relation_value(column_name)
                        # if old_val not in list_lookup, delete it
                        for child in relation_value:
                            old_val = getattr(child, shown_column[0])
                            list_old.append(old_val)
                            # delete
                            if old_val not in list_lookup:
                                if child in getattr(self, column_name):
                                    getattr(self, column_name).remove(child)
                                child.trash()
                            # edit if is_ordered
                            elif is_ordered:
                                for index, val in enumerate(list_lookup):
                                    if old_val == val:
                                        child._index = index + 1
                                        break
                        # if list_lookup not in old_val.shown_column[0], add it, set index if is_ordered
                        for index, val in enumerate(list_lookup):
                            if val not in list_old:
                                param = {shown_column[0] : val}
                                if is_ordered:
                                    param['_index'] = index + 1
                                new_record = ref_class(**param)
                                getattr(self, column_name).append(new_record)
                    # else, it must be tabular  
                    else:
                        # one to many
                        old_id_list             = [] # old id from database        
                        deleted_list            = [] # deleted id from variable (form)
                        relation_variable_list  = [] # from variable (form)
                        index_list              = [] # indexes from variable (form)
                        record_count            = 0  # total record count (from variable)
                        # by default bottle request doesn't automatically accept 
                        # POST with [] name
                        for variable_key in variable:
                            if hasattr(variable, 'getall') and variable_key[0:len(column_name)] == column_name and variable_key[-2:] == '[]':
                                # get list value
                                list_val = variable.getall(variable_key)                            
                                # make list of dictionary (as much as needed)
                                while record_count < len(list_val):
                                    relation_variable_list.append({})
                                    record_count +=1
                                new_variable_key = variable_key[len(column_name)+1:-2]
                                for i in xrange(record_count):
                                    relation_variable_list[i][new_variable_key] = list_val[i]
                        # special variables
                        if hasattr(variable, 'getall'):
                            old_id_list = variable.getall('_' + column_name + '_id[]')
                            deleted_list = variable.getall('_' + column_name + '_delete[]')
                            if issubclass(ref_class, Ordered_DB_Model):
                                index_list = variable.getall('_' + column_name + '_index[]')
                        # get relation
                        relation_value = self._get_relation_value(column_name)
                        for i in xrange(record_count):
                            old_id = old_id_list[i]
                            deleted = deleted_list[i] == "1"
                            relation_variable = relation_variable_list[i]
                            if is_ordered:
                                index = index_list[i]
                            ref_obj = None
                            for child in relation_value:
                                if isinstance(child, DB_Model):
                                    if child.id == old_id:
                                        ref_obj = child
                                        ref_obj.assign_from_dict(relation_variable)
                                        break
                            if ref_obj is None:
                                ref_obj = ref_class()
                                ref_obj.assign_from_dict(relation_variable)
                                getattr(self, column_name).append(ref_obj)
                            if is_ordered:
                                ref_obj._index = index
                            if deleted:
                                if ref_obj in getattr(self, column_name):
                                    getattr(self, column_name).remove(ref_obj)
                                ref_obj.trash()
                else:
                    # many to one
                    if column_name in variable and variable[column_name] != '':
                        value = variable[column_name]
                        if value != '':
                            ref_class = self._get_relation_class(column_name)
                            value = ref_class.find(value)
                        setattr(self, column_name, value)
    
    @classmethod
    def allow_list(cls):
        return cls.__allow_list__
    
    @classmethod
    def allow_new(cls):
        return cls.__allow_new__
    
    @property
    def allow_edit(self):
        if self._trashed == True:
            return False
        return self.__allow_edit__
    
    @property
    def allow_trash(self):
        if self._trashed == True:
            return False
        return self.__allow_trash__
    
    @property
    def allow_delete(self):
        return self.__allow_delete__

    @property
    def allow_untrash(self):
        if self._trashed == False:
            return False
        return self.__allow_untrash__
    
    def before_save(self):
        self.success = True
    
    def before_insert(self):
        self.success = True
    
    def before_update(self):
        self.success = True
    
    def before_trash(self):
        self.success = True
    
    def before_untrash(self):
        self.success = True
    
    def before_delete(self):
        self.success = True
    
    def after_save(self):
        self.success = True
    
    def after_insert(self):
        self.success = True
    
    def after_update(self):
        self.success = True
    
    def after_trash(self):
        self.success = True
    
    def after_untrash(self):
        self.success = True
    
    def after_delete(self):
        self.success = True
    
    def _get_relation_names(self):
        relation_names = []
        for relation_name in self.__mapper__.relationships._data:
            relation_names.append(relation_name)
        return relation_names
    
    def _get_relation_metadata(self, relation_name):
        return getattr(self.__mapper__.relationships, relation_name)
    
    def _get_relation_class(self, relation_name):
        return getattr(self.__class__, relation_name).property.mapper.class_
    
    def _get_relation_value(self, relation_name):
        return getattr(self, relation_name)
    
    def _get_actual_column_names(self):
        if not hasattr(self, '__column_names'):
            self.__column_names = []
            for column in self.__table__.columns:
                self.__column_names.append(column.name)
        return self.__column_names
    
    def _get_actual_column_metadata(self, column_name):
        if not hasattr(self, '__column'):
            self.__column = {}
            for column in self.__table__.columns:
                self.__column[column.name] = column
        return self.__column[column_name]
    
    def _get_actual_column_type(self, column_name):
        '''
        get actual sql column type
        '''
        return self._get_actual_column_metadata(column_name).type

    def is_coltype_match(self, column_name, cls):
        colmetadata = self._get_actual_column_metadata(column_name)
        if hasattr(colmetadata, 'is_coltype_match'):
            return colmetadata.is_coltype_match(cls)
        else:
            return False

    def is_coltype_attr_match(self, column_name, attr, value):
        colmetadata = self._get_actual_column_metadata(column_name)
        if hasattr(colmetadata, 'is_coltype_attr_match'):
            return colmetadata.is_coltype_attr_match(attr, value)
        else:
            return False

    def get_coltype_attr(self, column_name, attr, default = None):
        colmetadata = self._get_actual_column_metadata(column_name)
        if hasattr(colmetadata, 'get_coltype_attr'):
            return colmetadata.get_coltype_attr(attr)
        else:
            return default
    
    def _save_detail(self, already_saved_object):
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, DB_Model):
                # many to one
                if relation_value not in already_saved_object:
                    relation_value.save(already_saved_object)
            elif isinstance(relation_value, list):
                # many to one
                for child in relation_value:
                    if isinstance(child, DB_Model):
                        if child not in already_saved_object:
                            child.save(already_saved_object)
    
    @_db_operation_method  
    def save(self, already_saved_object = []):
        # is it insert or update?
        inserting = False
        if self._real_id is None:
            inserting = True
            # before insert
            if self.success:
                self.before_insert()
            # insert
            if self.success:
                self.session.add(self)
        else:
            #before update
            if self.success:
                self.before_update()
        # before save
        if self.success:
            self.before_save()
        # also upload the file
        if self.success:
            for column_name in self._get_actual_column_names():            
                colmetadata = self._get_actual_column_metadata(column_name)
                upload =  request.files.get(column_name)
                if self.is_coltype_match(column_name, Upload) and upload is not None:
                    save_uploaded_asset(column_name, path='uploads', application_name = self.__application_name__)
                    setattr(self, column_name, upload.filename)
        # save
        if self.success:
            self.session.commit()
        # generate id if not exists and re-save
        if self.success:
            if self.id is None:
                self.generate_id()
                self.session.commit()
        # after insert, after update and after save
        if self.success:
            if inserting:
                self.after_insert()
            else:
                self.after_update()
        if self.success:
            self.after_save()
        if self.success:
            # don't save the same object twice, it will make endless recursive
            already_saved_object.append(self)
            # also trigger save of relation
            self._save_detail(already_saved_object)
    
    @_db_operation_method
    def trash(self):
        if self.success:
            self.before_trash()
        if self.success:
            self._trashed = True
        if self.success:
            self.session.commit()
        if self.success:
            self.after_trash()
        if self.success:
            # also trash children
            for relation_name in self._get_relation_names():
                relation_value = self._get_relation_value(relation_name)
                if isinstance(relation_value, list):
                    for child in relation_value:
                        if isinstance(child, DB_Model):
                            child.trash()
                            child.save()
    
    @_db_operation_method
    def untrash(self):
        if self.success:
            self.before_untrash()
        if self.success:
            self._trashed = False
        if self.success:
            self.session.commit()
        if self.success:
            self.after_untrash()
        if self.success:
            # also untrash children
            for relation_name in self._get_relation_names():
                relation_value = self._get_relation_value(relation_name)
                if isinstance(relation_value, list):
                    for child in relation_value:
                        if isinstance(child, DB_Model):
                            child.untrash()
                            child.save()
    
    @_db_operation_method
    def delete(self):
        if self.success:
            self.before_delete()
        if self.success:
            self.session.delete(self)
        if self.success:
            self.session.commit()
        if self.success:
            self.after_delete()
        if self.success:
            # also delete children
            for relation_name in self._get_relation_names():
                relation_value = self._get_relation_value(relation_name)
                if isinstance(relation_value, list):
                    for child in relation_value:
                        if isinstance(child, DB_Model):
                            child.trash()
                            child.delete()
    
    def generate_prefix_id(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime(self.__id_prefix__)
    
    def generate_id(self):
        if self.id is None:
            prefix = self.generate_prefix_id()
            classobj = self.__class__
            # get maxid
            query = self.session.query(func.max(classobj.id).label("maxid")).filter(classobj.id.like(prefix+'%')).one()
            maxid = query.maxid
            if maxid is None:
                number = 0
            else:
                # get number part of maxid
                number = int(maxid[len(prefix):])
            # create newid
            newid = prefix + str(number+1).zfill(self.__id_digit__)
            self.id = newid
    
    def to_dict(self, **kwargs):
        '''
        Usage:
            model_instance.to_dict()
            model_instance.to_dict(include_relation = True, isoformat = True)
        '''
        include_relation = kwargs.pop('include_relation', False)
        isoformat = kwargs.pop('isoformat', False)
        dictionary = {}
        # get column value
        for column_name in self._get_actual_column_names():
            val = getattr(self, column_name)
            if isoformat and hasattr(val, 'isoformat'):
                val = val.isoformat()
            dictionary[column_name] = val
        # also include_relation
        if include_relation:
            kwargs = {'isoformat': isoformat}
            # also add relation to dictionary
            for relation_name in self._get_relation_names():
                relation = self._get_relation_value(relation_name)
                if isinstance(relation, DB_Model):
                    dictionary[relation_name] = relation.to_dict(**kwargs)
                elif isinstance(relation, list):
                    dictionary[relation_name] = []
                    for child in relation:
                        if isinstance(child, DB_Model):
                            dictionary[relation_name].append(child.to_dict(**kwargs))
                else:
                    dictionary[relation_name] = relation
        return dictionary
    
    def to_json(self, **kwargs):
        '''
        Usage:
            model_instance.to_json()
            model_instance.to_json(include_relation = True)
        '''
        kwargs['isoformat'] = True
        dictionary = self.to_dict(**kwargs)
        return json.dumps(dictionary)
    
    def build_label(self, column_name, **kwargs):
        ''' DON'T OVERRIDE THIS UNLESS YOU KNOW WHAT YOU DO
        This method is used to generate label
        '''
        # get custom_input if exists
        if hasattr(self, 'build_label_'+column_name):
            return getattr(self, 'build_label_'+column_name)(**kwargs)
        # look at __column_label__ property        
        if column_name in self.__column_label__:
            return self.__column_label__[column_name]
        # generate default label by replace '_' with ' ' in the column_name and make the first letter capitalized
        return column_name.replace('_', ' ').title()
    
    def _encode_input_attribute(self, attribute):
        html = ' '
        if isinstance(attribute, dict):
            for key in attribute:
                if isinstance(attribute[key], list):
                    attribute[key] = " ".join(attribute[key])
                html += key + ' = "' + attribute[key] + '" '
        html += ' '
        return html

    def _build_many_to_one_input(self, column_name, **kwargs):
        value = getattr(self, column_name) \
            if hasattr(self, column_name) and getattr(self, column_name) is not None \
            else ''
        kwargs          = self._build_input_attribute(column_name, kwargs)
        tabular         = kwargs.pop('tabular', False)
        input_attribute = kwargs.pop('input_attribute', {})
        input_name      = input_attribute.pop('name')
        input_id        = input_attribute.pop('id')
        input_class     = input_attribute.pop('class')
        # assemble input_selector
        input_selector  = '#' + input_id
        if input_class != '':
            input_selector += '.' + input_class
        # many to one
        ref_class = self._get_relation_class(column_name)
        option_obj = ref_class.get()
        option_count = ref_class.count()
        input_element = ''
        if option_count == 0:
            input_element += 'No option available'
        else:
            input_selector += '.form-control._chosen'
            options = {'': 'None'}
            for obj in option_obj:
                if isinstance(obj, DB_Model):
                    options[obj.id] = obj.as_text()
            value =  value.id if hasattr(value,'id') else ''
            input_element = HTML.select(input_selector, input_name, options, value)
            # add mutator
            self.generated_css.append(base_url('assets/chosen/chosen.min.css'))
            self.generated_js.append(base_url('assets/chosen/chosen.jquery.min.js'))
            self.generated_js += self._mutator_js('chosen', 
                    '$("._chosen").chosen();'
                )
        return input_element

    def _build_one_to_many_input(self, column_name, **kwargs):
        # one to many
        ref_class = self._get_relation_class(column_name)
        ref_obj = ref_class()
        # determine if the model is ordered
        is_ordered = isinstance(ref_obj, Ordered_DB_Model)
        # column name
        custom_label = self.__detail_column_label__[column_name]\
            if column_name in self.__detail_column_label__ else {}
        shown_column = self._get_detail_column_list(column_name)

        # if only one column to be shown and it is a relationship
        if len(shown_column) == 1 and shown_column[0] in ref_obj._get_relation_names():
            input_selector = '#field_' + column_name + '.form-control'
            input_name = column_name+'[]'
            # lookup class is the selection table, while child is association table
            lookup_class = ref_obj._get_relation_class(shown_column[0])
            # get values & options
            values = []
            options = {}
            for child in getattr(self, column_name):
                if isinstance(child, DB_Model):
                    values.append(getattr(child, shown_column[0]).id)
            for lookup in lookup_class.get():
                if isinstance(lookup, DB_Model):
                    options[lookup.id] = lookup.as_text()
            # create combobox
            style = ''
            # ordered
            if is_ordered:
                self.generated_css.append(base_url('assets/multiselect/css/ui.multiselect.css'))
                self.generated_js.append(base_url('assets/multiselect/js/ui.multiselect.js'))
                self.generated_js += self._mutator_js('ordered', 
                        '$("._ordered").multiselect();'
                    )
                input_selector += '._ordered'
                style = 'min-height:150px;'
            # unordered
            else:
                self.generated_css.append(base_url('assets/chosen/chosen.min.css'))
                self.generated_js.append(base_url('assets/chosen/chosen.jquery.min.js'))
                self.generated_js += self._mutator_js('chosen', 
                        '$("._chosen").chosen();'
                    )
                input_selector += '._chosen'
            # create input
            input_element = HTML.select(input_selector, input_name, options, values, True, style = style)
        # else, it must be tabular  
        else:

            ref_obj.generate_tabular_label(state = 'form', shown_column = self._get_detail_column_list(column_name), custom_label = custom_label)
            
            # define several HTML DOM's properties
            div_empty_selector      = '#_div_empty_' + column_name
            div_empty_style         = '' 
            div_control_selector    = '#_div_control_' + column_name
            a_new_selector          = '#_' + column_name + '_add' + '.btn .btn-default ._new_row'
            a_new_caption           = 'New ' + self.build_label(column_name)
            table_selector          = '#_table_' + column_name + '.table'
            table_style             = ''
            tbody_selector          = '#_' + column_name + '_tbody'
            # only one should be shown, table or div_empty
            if len(getattr(self, column_name)) == 0:
                table_style = 'display:none;'
            else:
                div_empty_style = 'display:none;'
                div_control_selector += '.pull-right'

            # div empty
            div_empty   = HTML.div(div_empty_selector, 'No Data', style = div_empty_style)
            # div control
            div_control = HTML.div(div_control_selector, 
                    HTML.a(a_new_selector, '#', HTML.tag('i.glyphicon.glyphicon-plus') + a_new_caption)
                )
            
            # thead
            th = ref_obj.generated_html
            if is_ordered:
                th += HTML.th('Order', style="width:50px;")
            th += HTML.th('Delete', style="width:50px;")
            thead = HTML.thead(HTML.tr(th))

            # tbody
            tr = ''
            new_row_index = 0
            for row_index, child in enumerate(getattr(self, column_name)):
                new_row_index += 1
                child.generate_tabular_input(state = 'form', shown_column = shown_column, parent_column_name = column_name)
                # td
                td = child.generated_html
                # add ordering
                if is_ordered:
                    input_selector  = '._' + column_name + '_index #_' + column_name + '_index_' + str(row_index) 
                    input_name      = '_'+column_name+'_index[]'
                    a_up_selector   = '._' + column_name + '_up'
                    a_down_selector = '._' + column_name + '_down'
                    a_property      = {'row-index' : str(row_index)}
                    td += HTML.td(
                            HTML.input_hidden(input_selector, input_name, str(row_index)) +\
                            HTML.a(a_up_selector, '#', HTML.tag('i.glyphicon.glyphicon-arrow-up'), **a_property ) +\
                            HTML.a(a_down_selector, '#', HTML.tag('i.glyphicon.glyphicon-arrow-down'), **a_property )
                        )
                # add control
                input_id_selector         = '._' + column_name + '_id'
                input_id_name             = '_' + column_name + '_id[]'
                input_deleted_name        = '_' + column_name + '_delete[]'
                checkbox_property         = {'class' : '_' + column_name + '_delete'}
                td += HTML.td(
                        HTML.input_hidden(input_id_selector, input_id_name, str(child.id)) +
                        HTML.input_hidden('.deleted', input_deleted_name, '0') +
                        HTML.label(
                                HTML.input_checkbox(**checkbox_property)
                            )
                    )
                # add to tr
                tr += HTML.tr(td)
            tbody = HTML.tbody(tbody_selector, tr)

            # table
            table = HTML.table(table_selector, thead + tbody, style = table_style)

            # input element
            input_element  = div_empty + div_control + table

            # what should be added when add row clicked
            ref_obj.generate_tabular_input(state = 'form', shown_column = self._get_detail_column_list(column_name), parent_column_name = column_name)
            new_row  = '\'<tr>'
            new_row += ref_obj.generated_html

            # merge detail's css & js into main css & js
            self.generated_js  += ref_obj.generated_js
            self.generated_css += ref_obj.generated_css

            # order column
            last_index_varname = '_' + column_name + '_last_index'
            if is_ordered:
                concat_last_index_varname = '\' + ' + last_index_varname + '+ \''
                new_row += '<td>'
                new_row += '<input class="_'+column_name+'_index" id="_'+column_name+'_index_'+concat_last_index_varname+'" type="hidden" name="_'+column_name+'_index[]" value="'+concat_last_index_varname+'" />'
                new_row += '<a class="_'+column_name+'_up" row-index="'+concat_last_index_varname+'" href="#"><i class="glyphicon glyphicon glyphicon-arrow-up"></i></a>'
                new_row += '<a class="_'+column_name+'_down" row-index="'+concat_last_index_varname+'" href="#"><i class="glyphicon glyphicon glyphicon-arrow-down"></i></a>'
                new_row += '</td>'
            # delete column
            new_row += '<td>'
            new_row += '    <input type="hidden" name="_' + column_name + '_id[]" value="" />'
            new_row += '    <input class="deleted" type="hidden" name="_' + column_name + '_delete[]" value="0" />'
            new_row += '    <label><input type="checkbox" class="_' + column_name + '_delete"></label>'
            new_row += '</td>'
            new_row += '</tr>\''
            script  = ''
            if is_ordered:
                script += 'var ' + last_index_varname + ' = ' + str(new_row_index) + ';'
            # delete event
            script += '$("._' + column_name + '_delete").live("click", function(event){'
            script += '    var input = $(this).parent().parent().children(".deleted");'
            script += '    if($(this).prop("checked")){'
            script += '        input.val("1");'
            script += '    }else{'
            script += '        input.val("0");'
            script += '    }'
            script += '});'
            # add event
            script += '$("#_' + column_name + '_add").click(function(event){'
            script += '    $("#_' + column_name + '_tbody").append(' + new_row + ');'
            script += '    $("#_div_control_' + column_name + '").addClass("pull-right");'
            script += '    $("#_div_empty_' + column_name + '").hide();'
            script += '    $("#_table_' + column_name + '").show();'
            if is_ordered:
                script += '    '+last_index_varname+'++;'
            script += '    event.preventDefault();'
            script += '});'
            # up event
            script += '$("a._'+column_name+'_up").live("click",function(event){'
            script += '    var row_index = $(this).attr("row-index");'
            script += '    var current_tr = $(this).parent().parent();'
            script += '    var prev_tr = current_tr.prev();'
            script += '    if(prev_tr.length > 0){'
            script += '        current_tr.insertBefore(prev_tr);'
            script += '        current_element = current_tr.find("td ._'+column_name+'_index");'
            script += '        prev_element = prev_tr.find("td ._'+column_name+'_index");'
            script += '        current_element_val = current_element.val();'
            script += '        prev_element_val = prev_element.val();'
            script += '        prev_element.val(current_element_val);'
            script += '        current_element.val(prev_element_val);'
            script += '    }'
            script += '    event.preventDefault();'
            script += '});'
            # down event
            script += '$("a._'+column_name+'_down").live("click",function(event){'
            script += '    var row_index = $(this).attr("row-index");'
            script += '    var current_tr = $(this).parent().parent();'
            script += '    var next_tr = current_tr.next();'
            script += '    if(next_tr.length > 0){'
            script += '        current_tr.insertAfter(next_tr);'
            script += '        current_element = current_tr.find("td ._'+column_name+'_index");'
            script += '        next_element = next_tr.find("td ._'+column_name+'_index");'
            script += '        current_element_val = current_element.val();'
            script += '        next_element_val = next_element.val();'
            script += '        next_element.val(current_element_val);'
            script += '        current_element.val(next_element_val);'
            script += '    }'
            script += '    event.preventDefault();'
            script += '});'
            self.generated_js += script
        return input_element

    def _mutator_js(self, mutation_name, script):
        return '$(document).ready(function(){' +\
            '    function _mutate_' + mutation_name + '(){' +script + '}' +\
            '    _mutate_' + mutation_name + '();' +\
            '    $("._new_row").live("click", function(event){' +\
            '        _mutate_' + mutation_name + '();' +\
            '    });' +\
            '});'

    def _build_column_input(self, column_name, **kwargs):
        value = getattr(self, column_name) \
            if hasattr(self, column_name) and getattr(self, column_name) is not None \
            else ''
        kwargs          = self._build_input_attribute(column_name, kwargs)
        tabular         = kwargs.pop('tabular', False)
        input_attribute = kwargs.pop('input_attribute', {})
        input_name      = input_attribute.pop('name')
        input_id        = input_attribute.pop('id')
        input_class     = input_attribute.pop('class')
        # assemble input_selector
        input_selector  = '#' + input_id
        if input_class != '':
            input_selector += '.' + input_class
        # get placeholder
        placeholder = self.build_label(column_name, **kwargs)
        input_element = ''
        # check type
        actual_column_type = self._get_actual_column_type(column_name)
        # get metadata and coltype
        colmetadata = self._get_actual_column_metadata(column_name)
        coltype = colmetadata._coltype
        # Option
        if self.is_coltype_match(column_name, Option):
            input_selector += '.form-control._chosen'
            if coltype.multiple:
                value = value.split(', ')
            input_element = HTML.select(input_selector, input_name, coltype.options, value, coltype.multiple)
            # add mutator
            self.generated_css.append(base_url('assets/chosen/chosen.min.css'))
            self.generated_js.append(base_url('assets/chosen/chosen.jquery.min.js'))
            self.generated_js += self._mutator_js('chosen', 
                    '$("._chosen").chosen();'
                )
        # Upload
        elif self.is_coltype_match(column_name, Upload):
            input_selector += '._file-input'
            input_element = HTML.div(self.build_representation(column_name)) if value is not None else ''
            input_element += HTML.input_file(input_selector, input_name)
            # add mutator script
            self.generated_js.append(base_url('assets/jquery-ui-bootstrap/third-party/jQuery-UI-FileInput/js/enhance.min.js'))
            self.generated_js.append(base_url('assets/jquery-ui-bootstrap/third-party/jQuery-UI-FileInput/js/fileinput.jquery.js'))
            self.generated_js += self._mutator_js('file_input', 
                    '$("._file-input:not(._mutated)").customFileInput({button_position : "right"});' +\
                    '$("._file-input").addClass("_mutated");'
                )
        # RichText
        elif self.is_coltype_match(column_name, RichText):
            input_selector += '.form-control._richtext-textarea'
            input_element = HTML.textarea(input_selector, input_name, value, placeholder)
            # add mutator script
            self.generated_js.append(base_url('assets/ckeditor/ckeditor.js'))
            self.generated_js.append(base_url('assets/ckeditor/adapters/jquery.js'))
            self.generated_js += self._mutator_js('richtext_textarea', 
                    '$("._richtext-textarea").ckeditor();'
                )
        # Code
        elif self.is_coltype_match(column_name, Code):
            theme = self.get_coltype_attr(column_name, 'theme', 'monokai')
            language = self.get_coltype_attr(column_name, 'language', 'python')
            input_selector += '.form-control._code-textarea._code_' + language + '_' + theme
            input_element = HTML.textarea(input_selector, input_name, value, placeholder)
            # add mutator script
            self.generated_js.append(base_url('assets/jquery-ace/ace/ace.js'))
            self.generated_js.append(base_url('assets/jquery-ace/ace/theme-' + theme + '.js'))
            self.generated_js.append(base_url('assets/jquery-ace/ace/mode-' + language + '.js'))
            self.generated_js.append(base_url('assets/jquery-ace/jquery-ace.min.js'))
            self.generated_js += self._mutator_js('code_' + language + '_' + theme + '_textarea',
                    '$("._code_' + language + '_' + theme + '").ace({' +\
                    '    theme: "' + theme + '",' +\
                    '    lang: "' + language + '",' +\
                    '});'+\
                    '$("._code_' + language + '_' + theme + '").each(function(){' +\
                    '    var ace = $(this).data("ace").editor.ace;' +\
                    '    ace.setOptions({"minLines": 5, "maxLines": 30, "fontSize": 16});' +\
                    '});'
                )
        # Password
        elif self.is_coltype_match(column_name, Password):
            input_selector += '.form-control'
            input_element = HTML.input_password(input_selector, input_name, value, placeholder)        
        # Boolean
        elif isinstance(actual_column_type, Boolean):
            input_element = HTML.input_hidden(input_name, 0) +\
                HTML.input_checkbox(input_selector, input_name, 1, bool(value))
        # Text
        elif isinstance(actual_column_type, Text):
            input_selector += '.form-control._autosize-textarea'
            input_element = HTML.textarea(input_selector, input_name, value, placeholder)
            # add mutator script
            self.generated_js.append(base_url('assets/autosize/jquery.autosize.min.js'))
            self.generated_js += self._mutator_js('autosize_textarea', 
                    '$("._autosize-textarea").autosize();'
                )
        # Others (Date, Integer, and normal string)
        else:
            value = str(encode_string(value))
            # DateTime
            if isinstance(actual_column_type, DateTime):
                input_selector += '.form-control._datetime-input'
                # add mutator script
                self.generated_js.append(base_url('assets/jquery-ui-timepicker-addon.js'))
                self.generated_js += self._mutator_js('datetime_input',
                        '$("._datetime-input").datetimepicker({' +\
                        '    defaultDate: null,'+\
                        '    changeMonth: true,'+\
                        '    changeYear: true,'+\
                        '    numberOfMonths: 1,'+\
                        '    dateFormat: "yy-mm-dd",'+\
                        '    timeFormat: "HH:mm:ss",'+\
                        '    yearRange: "c-50:c+50",'+\
                        '});'
                    )
            # Date
            elif isinstance(actual_column_type, Date):
                input_selector += '.form-control._date-input'
                # add mutator script
                self.generated_js += self._mutator_js('date_input', 
                        '$("._date-input").datepicker({' +\
                        '    defaultDate: null,'+\
                        '    changeMonth: true,'+\
                        '    changeYear: true,'+\
                        '    numberOfMonths: 1,'+\
                        '    dateFormat: "yy-mm-dd",'+\
                        '    yearRange: "c-50:c+50",'+\
                        '});'
                    )
            # Integer
            elif isinstance(actual_column_type, Integer):
                input_selector += '._integer-input'
                value = '0' if value == '' else value
                # add mutator script
                self.generated_js += self._mutator_js('integer_input', 
                        '$("._integer-input").spinner();'
                    )
            # Normal String
            else:            
                input_selector += '.form-control'

            # generate input element
            input_element = HTML.input_text(input_selector, input_name, value, placeholder)

        return input_element


    def _build_input_attribute(self, column_name, kwargs):
        kwargs['tabular']           = kwargs.pop('tabular', False)
        input_attribute             = kwargs.pop('input_attribute', {})
        input_attribute['name']     = input_attribute['name'] if 'name' in input_attribute else column_name
        input_attribute['id']       = input_attribute['id'] if 'id' in input_attribute else 'field_' + column_name
        input_attribute['class']    = input_attribute['class'] if 'class' in input_attribute else ''
        kwargs['input_attribute']   = input_attribute
        return kwargs
    
    def build_input(self, column_name, **kwargs):
        ''' DON'T OVERRIDE THIS UNLESS YOU KNOW WHAT YOU DO
        This method is used to generate input
        '''
                
        # return custom input if user has already define the function
        if hasattr(self, 'build_input_'+column_name):
            kwargs = self._build_input_attribute(column_name, kwargs)
            return getattr(self, 'build_input_'+column_name)(**kwargs)
        # otherwise, return default input
        
        html = ''
        if column_name in self._get_relation_names():
            relation_metadata = self._get_relation_metadata(column_name)
            if relation_metadata.uselist:
                html = self._build_one_to_many_input(column_name, **kwargs)               
            else:
                html = self._build_many_to_one_input(column_name, **kwargs)
        else:
            html = self._build_column_input(column_name, **kwargs)
        return html
    
    def build_labeled_input(self, column_name, **kwargs):
        label = self.build_label(column_name, **kwargs)
        return HTML.div('.form-group .row .container .col-xs-12 .col-sm-12 .col-md-12 .col-lg-12',
                    HTML.label('.col-xs-12 .col-sm-12 .col-md-3 .col-lg-3 .control-label', label) +\
                    HTML.div('.col-xs-12 .col-sm-12 .col-md-9 .col-lg-9',
                            self.build_input(column_name, **kwargs)
                        )
                )

    def _build_one_to_many_representation(self, column_name, **kwargs):
        value = getattr(self, column_name) if hasattr(self, column_name) else None
        if isinstance(value, list):
            if len(value) == 0:
                value = None
            else:
                # get children
                children = getattr(self,column_name)
                # ref_obj, custom_label and shown_column
                ref_obj = self._get_relation_class(column_name)()
                custom_label = self.__detail_column_label__[column_name]\
                    if column_name in self.__detail_column_label__ else {}
                shown_column = self._get_detail_column_list(column_name)
                # if only one column to be shown
                if len(shown_column) == 1:
                    if len(children) == 0:
                        value = 'No Data'
                    elif len(children) == 1:
                        child = children[0]
                        if shown_column[0] not in child._get_relation_names():
                            value = child.quick_preview()
                        else:
                            value = child.build_representation(shown_column[0])
                    else:
                        is_ordered = isinstance(ref_obj, Ordered_DB_Model);
                        value = []
                        for child in children:
                            # determine single value
                            if shown_column[0] not in child._get_relation_names():
                                single_value = child.quick_preview()
                            else:
                                single_value = child.build_representation(shown_column[0])

                            if is_ordered:
                                value.append(HTML.li(single_value))
                            else:
                                value.append(single_value)

                        if is_ordered:
                            value = HTML.ol('.container', value)
                        else:
                            value = ', '.join(value)
                else:
                    # generate thead
                    ref_obj.generate_tabular_label(state = 'view',
                        shown_column = shown_column, 
                        custom_label = custom_label)
                    thead = HTML.thead(HTML.tr(ref_obj.generated_html))
                    # generate tbody
                    tr = []
                    for child in children:
                        child.generate_tabular_representation(state = 'view', 
                            shown_column = self._get_detail_column_list(column_name))
                        tr.append(HTML.tr(child.generated_html))
                    tbody = HTML.tbody(tr)
                    # generate tfoot
                    if(hasattr(self, 'build_tabular_footer_'+column_name)):
                        tfoot = HTML.tfoot(
                                getattr(self,'build_tabular_footer_'+column_name)(state = 'view')
                            )
                    else:
                        tfoot = ''
                    # generate table
                    value = HTML.table('.table', [thead, tbody, tfoot])
        return value

    def _build_many_to_one_representation(self, column_name, **kwargs):
        value = getattr(self, column_name) if hasattr(self, column_name) else None
        if isinstance(value, DB_Model):
            value = value.quick_preview()
        return value

    def _build_column_representation(self, column_name, **kwargs):
        # get value      
        value = getattr(self, column_name) if hasattr(self, column_name) else None
        if self.is_coltype_match(column_name, RichText):
            input_selector = '#_field_' + column_name + '.form-control._richtext-textarea'
            value = '' if value is None else value
            value = HTML.textarea(input_selector, '', value)
            # add mutator script
            self.generated_js.append(base_url('assets/ckeditor/ckeditor.js'))
            self.generated_js.append(base_url('assets/ckeditor/adapters/jquery.js'))
            self.generated_js += self._mutator_js('richtext_textarea', 
                    '$("._richtext-textarea").ckeditor({readOnly:true});'
                )
        # Code
        elif self.is_coltype_match(column_name, Code):
            theme = self.get_coltype_attr(column_name, 'theme', 'monokai')
            language = self.get_coltype_attr(column_name, 'language', 'python')
            input_selector = '.form-control._code-textarea._code_' + language + '_' + theme
            value = '' if value is None else value
            value = HTML.textarea(input_selector, '', value)
            # add mutator script
            self.generated_js.append(base_url('assets/jquery-ace/ace/ace.js'))
            self.generated_js.append(base_url('assets/jquery-ace/ace/theme-' + theme + '.js'))
            self.generated_js.append(base_url('assets/jquery-ace/ace/mode-' + language + '.js'))
            self.generated_js.append(base_url('assets/jquery-ace/jquery-ace.min.js'))
            self.generated_js += self._mutator_js('code_' + language + '_' + theme + '_textarea',
                    '$("._code_' + language + '_' + theme + '").ace({' +\
                    '    theme: "' + theme + '",' +\
                    '    lang: "' + language + '",' +\
                    '});'+\
                    '$("._code_' + language + '_' + theme + '").each(function(){' +\
                    '    var ace = $(this).data("ace").editor.ace;' +\
                    '    ace.setOptions({"minLines": 5, "maxLines": 30, "fontSize": 16});' +\
                    '    ace.setReadOnly(true);' +\
                    '});'
                )
        elif isinstance(value, unicode) or isinstance(value, str):
            value = HTML.presented_html_code(value)
        colmetadata = self._get_actual_column_metadata(column_name)
        if value is None:
            value = 'Not available'
        elif self.is_coltype_match(column_name, Upload):
            # get inner value
            if self.is_coltype_attr_match(column_name, 'is_image', True):
                inner_html = HTML.img(
                        base_url(self.__application_name__+ '/assets/uploads/' + value),
                        style = 'max-width:100px;'
                    )
            else:
                inner_html = value
            # generate link if necessary
            if self.is_list_state():
                value = inner_html
            else:
                value = HTML.a(
                        base_url(self.__application_name__ + '/assets/uploads/' + value),
                        inner_html,
                        target = 'blank'
                    )
        return value

    
    def build_representation(self, column_name, **kwargs):
        ''' DON'T OVERRIDE THIS UNLESS YOU KNOW WHAT YOU DO
        This method is used to generate representation
        '''        
        value = None        
        # return custom_representation if exists
        if hasattr(self, 'build_representation_'+column_name):
            value = getattr(self, 'build_representation_'+column_name)(**kwargs)
        # if it is relation, retrieve it
        elif column_name in self._get_relation_names():
            relation_metadata = self._get_relation_metadata(column_name)
            # one to many
            if relation_metadata.uselist:
                value = self._build_one_to_many_representation(column_name, **kwargs)
            # many to one
            else:
                value = self._build_many_to_one_representation(column_name, **kwargs)
        else:
            # get metadata and coltype
            value = self._build_column_representation(column_name, **kwargs)            
        # If not available
        value = str(encode_string(value)) if value is not None else 'Not available'
        return value
    
    def build_labeled_representation(self, column_name, **kwargs):
        label = self.build_label(column_name, **kwargs)
        return HTML.div('.form-group .row .container .col-xs-12 .col-sm-12 .col-md-12 .col-lg-12',
                    HTML.label('.col-xs-12 .col-sm-12 .col-md-3 .col-lg-3 .control-label', label) +\
                    HTML.div('.col-xs-12 .col-sm-12 .col-md-9 .col-lg-9',
                            self.build_representation(column_name, **kwargs)
                        )
                )
    
    def reset_generated(self):
        self._generated_html = ''
        self._generated_js = JS_Resource()
        self._generated_css = CSS_Resource()
    
    def _include_default_resource(self):
        base_url = base_url()
        self._generated_js.append_compiled(asset.JQUI_BOOTSTRAP_SCRIPT)
        self._generated_js.append_compiled(asset.KOKORO_CRUD_SCRIPT)
        self._generated_css.append_compiled(asset.JQUI_BOOTSTRAP_STYLE)
        self._generated_css.append_compiled(asset.KOKORO_CRUD_STYLE)

    def quick_preview(self):
        '''
        Quick preview of record, override this
        '''
        column_list = self._column_list
        if len(column_list) >1:
            value = getattr(self, column_list[1])
            if isinstance(value, DB_Model):
                value = value.quick_preview()
            return str(encode_string(value))
        return self.as_text()

    def as_text(self):
        '''
        Text preview of record, no html tag. Override this if necessary
        '''
        column_list = self._column_list
        if len(column_list) >1:
            value = getattr(self, column_list[1])
            if isinstance(value, DB_Model):
                value = value.quick_preview()
            return str(encode_string(value))
        return self.id        
    
    def _get_tabular_column_names_by_state(self, state = None):
        '''
        state: "view" or "form"
        '''
        if state is None or state == 'view':
            if self.__tabular_shown_column__ is not None:
                column_names = self.__tabular_shown_column__
            else:
                column_names = self._column_list
        elif state == 'form':
            if self.__tabular_form_column__ is not None:
                column_names = self.__tabular_form_column__
            else:
                column_names = self._column_list
        return column_names
    
    def generate_tabular_label(self, **kwargs):
        include_resource = kwargs.pop('_include_default_resource', False)
        shown_column = kwargs.pop('shown_column', [])
        custom_label = kwargs.pop('custom_label', {})
        # prepare resource
        self.reset_generated()
        if include_resource:
            self._include_default_resource()
        # create html
        html  = ''
        if len(shown_column) == 0:
            shown_column = self._column_list
        for column_name in shown_column:
            if column_name in self._get_relation_names() and self._get_relation_class(column_name) == self.__class__:
                continue
            if column_name in custom_label:
                label = custom_label[column_name]
            else:
                label = self.build_label(column_name)
            html += HTML.th(label)
        self.generated_html = html
    
    def generate_tabular_representation(self, **kwargs):
        include_resource = kwargs.pop('_include_default_resource', False)
        shown_column = kwargs.pop('shown_column', [])
        # prepare resource
        self.reset_generated()
        if include_resource:
            self._include_default_resource()
        # create html
        html  = ''
        if len(shown_column) == 0:
            shown_column = self._column_list
        for column_name in shown_column:
            if column_name in self._get_relation_names() and self._get_relation_class(column_name) == self.__class__:
                continue
            html += HTML.td(self.build_representation(column_name))
        self.generated_html = html
    
    def generate_tabular_input(self, **kwargs):
        include_resource = kwargs.pop('_include_default_resource', False)
        shown_column = kwargs.pop('shown_column', [])
        # prepare resource
        self.reset_generated()
        if include_resource:
            self._include_default_resource()
        # create html
        html  = ''
        parent_column_name = kwargs.pop('parent_column_name', '')
        if len(shown_column) == 0:
            shown_column = self._column_list
        for column_name in shown_column:
            if column_name in self._get_relation_names() and self._get_relation_class(column_name) == self.__class__:
                continue
            input_name = parent_column_name + '_' + column_name + '[]' if parent_column_name != '' else column_name+'[]'
            input_attribute = {'name': input_name}
            html += HTML.td(self.build_input(column_name, input_attribute = input_attribute, tabular = True))
        self.generated_html = html
    
    def generate_input_components(self, state = None, include_resource = False, **kwargs):
        '''
        Input view of record
        '''
        # prepare resource
        self.reset_generated()
        if include_resource:
            self._include_default_resource()
        # build html
        html = ''
        for column_name in self._column_list:
            html += self.build_labeled_input(column_name)
        self.generated_html = html
        
    
    def generate_detail_view(self, include_resource = False, **kwargs):
        '''
        Detail view of record, override this with care
        '''
        # prepare resource
        self.reset_generated()
        if include_resource:
            self._include_default_resource()
        # build html
        html = ''
        for column_name in self._column_list:
            html += self.build_labeled_representation(column_name)
        self.generated_html = HTML.div('.row .container', html)

class Ordered_DB_Model(DB_Model):
    _index          = Column(Integer, index=True)
    # properties
    __group_by__    = None
    __abstract__    = True
    
    def save(self, already_saved_object = []):
        classobj = self.__class__
        index = self._index
        real_id = self._real_id
        if self.__group_by__ is not None and hasattr(classobj, self.__group_by__):
            group_by_field = getattr(classobj, self.__group_by__)
        else:
            group_by_field = None
        # get new_index
        if self._index is None:
            # get maxid
            query = self.session.query(func.max(classobj._index).label("max_index"))
            if group_by_field is None:
                query = query.one()
            else:
                group_by_value = getattr(self, self.__group_by__)
                query = query.filter(group_by_field==group_by_value).one()
            max_index = query.max_index
            if max_index is None:
                max_index = 0
            else:
                max_index = int(max_index)
            index = max_index+1
            # increase self._index if index is collide
            while True:
                query = self.session.query(func.count(classobj._index).label("duplicate_count"))
                if group_by_field is not None:
                    group_by_value = getattr(self, self.__group_by__)
                    query = query.filter(group_by_field==group_by_value, classobj._index == index, classobj._real_id != real_id)
                else:
                    query = query.filter(classobj._index == index, classobj._real_id != real_id)
                query = query.one()
                duplicate_count = query.duplicate_count
                if duplicate_count == 0:
                    break
                else:
                    index += 1
            self._index = index
        DB_Model.save(self, already_saved_object)
    
    @classmethod
    def get(cls, *criterion, **kwargs):
        if 'order_by' not in kwargs:
            kwargs['order_by'] = cls._index
        return super(Ordered_DB_Model, cls).get(*criterion, **kwargs)
    
    def move_up(self):
        if self._real_id is None or self._index is None:
            pass
        classobj = self.__class__
        if self.__group_by__ is not None and hasattr(classobj, self.__group_by__):
            group_by_field = getattr(classobj, self.__group_by__)
        else:
            group_by_field = None
        # get max_index of record with index less than this object
        query = self.session.query(func.max(classobj._index).label("max_index"))
        if group_by_field is None:
            query = query.filter(classobj._index < self._index).one()
        else:
            group_by_value = getattr(self, self.__group_by__)
            query = query.filter(classobj._index < self._index, group_by_field==group_by_value).one()
        max_index = query.max_index
        if max_index is None:
            max_index = 0
        else:
            max_index = int(max_index)
        # get object with index =  max_index
        query = self.session.query(classobj)
        if group_by_field is not None:
            group_by_value = getattr(self, self.__group_by__)
            query = query.filter(group_by_field == group_by_value, classobj._index == max_index)
        else:
            query = query.filter(classobj._index == max_index)
        # neighbor
        try:
            neighbor = query.one()
            current_index = self._index
            self._index = neighbor._index
            neighbor._index = current_index
            DB_Model.save(self)
            DB_Model.save(neighbor)
            return True
        except NoResultFound, _:
            return False
    
    def move_down(self):
        if self._real_id is None or self._index is None:
            pass
        classobj = self.__class__
        if self.__group_by__ is not None and hasattr(classobj, self.__group_by__):
            group_by_field = getattr(classobj, self.__group_by__)
        else:
            group_by_field = None
        # get min_index of record with index less than this object
        query = self.session.query(func.min(classobj._index).label("min_index"))
        if group_by_field is None:
            query = query.filter(classobj._index > self._index).one()
        else:
            group_by_value = getattr(self, self.__group_by__)
            query = query.filter(classobj._index > self._index, group_by_field==group_by_value).one()
        min_index = query.min_index
        if min_index is None:
            min_index = 0
        else:
            min_index = int(min_index)
        # get object with index =  min_index
        query = self.session.query(classobj)
        if group_by_field is not None:
            group_by_value = getattr(self, self.__group_by__)
            query = query.filter(group_by_field == group_by_value, classobj._index == min_index)
        else:
            query = query.filter(classobj._index == min_index)
        # neighbor
        try:
            neighbor = query.one()
            current_index = self._index
            self._index = neighbor._index
            neighbor._index = current_index
            DB_Model.save(self)
            DB_Model.save(neighbor)
            return True
        except NoResultFound, _:
            return False

def auto_migrate(engine):
    print('    %s%s WARNING %s%s%s : You are using auto_migrate()\n    Note that not all operation supported. Be prepared to do things manually.\n    Using auto_migration in production mode is not recommended.%s%s' %(Fore.BLACK, Back.GREEN, Fore.RESET, Back.RESET, Fore.GREEN, Fore.RESET, Fore.MAGENTA))
    # make model_meta & db_meta
    DB_Model.metadata.create_all(bind=engine)
    model_meta = DB_Model.metadata
    db_meta = MetaData()
    db_meta.reflect(bind=engine)
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    # default parameters
    default_column_names = ['_real_id', '_trashed', '_created_at', '_updated_at', 'id']
    column_properties = ['key', 'primary_key', 'nullable', 'default',
                         'server_default', 'server_onupdate', 'index',
                         'unique', 'system', 'quote', 'doc', 'onupdate',
                         'autoincrement', 'constraints', 'foreign_keys']
    for model_table_name in model_meta.tables:
        # get model_table from model_meta
        model_table = model_meta.tables[model_table_name]
        db_table = None
        # make model_table with alembic if necessary
        if model_table_name not in db_meta.tables:
            try:
                op.create_table(
                    model_table_name,
                    Column('_real_id', Integer, primary_key = True),
                    Column('_trashed', Boolean, default = False),
                    Column('_created_at', DateTime, default=func.now()),
                    Column('_updated_at', DateTime, default=func.now(), onupdate=func.now()),
                    Column('id', String(35), unique = True)
                )
            except Exception, e:
                logger.error('    Fail to make table: %s, please add it manually' % (model_table_name))
                logger.error('    Error message : %s' % (str(e)))
        else:
            db_table = db_meta.tables[model_table_name]
        for model_column in model_table.columns:
            # don't create or alter default columns
            if model_column.name in default_column_names:
                continue
            # get model_column properties
            model_column_kwargs = {}
            for prop in column_properties:
                if hasattr(model_column, prop):
                    model_column_kwargs[prop] = getattr(model_column, prop)
            # make model_column with alembic if necessary
            if model_column.name not in db_meta.tables[model_table_name].columns:
                try:
                    op.add_column(model_table_name, Column(model_column.name, model_column.type, **model_column_kwargs))
                except:
                    try:
                        # sometime foreign_keys and constraints just doesn't work
                        model_column_kwargs.pop('foreign_keys')
                        model_column_kwargs.pop('constraints')
                        op.add_column(model_table_name, Column(model_column.name, model_column.type, **model_column_kwargs))
                    except Exception, e:
                        logger.error('    Fail to make column %s.%s, please add it manually' % (model_table_name, model_column.name))
                        logger.error('    Error message : %s' % (str(e)))
            else:
                # get db_column information
                db_column = None
                if db_table is not None:
                    for column in db_table.columns:
                        if column.name == model_column.name:
                            db_column = column
                            break
                db_column_kwargs = {}
                for prop in column_properties:
                    db_column_kwargs[prop] = getattr(db_column, prop)
                # is alter column needed?
                need_alter = str(model_column.type) != str(db_column.type) or model_column_kwargs['nullable'] != db_column_kwargs['nullable']
                if need_alter:
                    # alter model_table with alembic
                    try:
                        op.alter_column(model_table_name, 
                                        model_column.name, 
                                        nullable = model_column_kwargs['nullable'], # None, 
                                        server_default = False, 
                                        new_column_name = None, 
                                        type_ = model_column.type, # None 
                                        existing_type=None, 
                                        existing_server_default=False, 
                                        existing_nullable=None)
                    except Exception, e:
                        logger.error('    Fail to alter column %s.%s, please alter it manually.\n      Old type: %s, new type: %s' % (model_table_name, model_column.name, str(db_column.type), str(model_column.type)))
                        logger.error('    Error message, ' + str(e))
    print(Fore.RESET)