from sqlalchemy import create_engine, Column, func, BIGINT, BigInteger, BINARY, Binary,\
    BOOLEAN, Boolean, DATE, Date, DATETIME, DateTime, FLOAT, Float,\
    INTEGER, Integer, VARCHAR, String, TEXT, Text, MetaData
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from alembic.migration import MigrationContext
from alembic.operations import Operations
import datetime, time, json, sys, os, asset
from kokoropy import Fore, Back, base_url

# initialize logger
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create Base
Base = declarative_base()
        
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
    __echo__ = True
    __prefix_of_id__        = '%Y%m%d-'
    __digit_num_of_id__     = 5
    # columns to be shown
    __shown_column__            = None
    __form_column__             = None
    __insert_column__           = None
    __update_column__           = None
    __virtual_shown_column__    = None
    __virtual_form_column__     = None
    __virtual_insert_column__   = None
    __virtual_update_column__   = None
    __excluded_shown_column__   = None
    __excluded_form_column__    = None
    __excluded_insert_column__  = None
    __excluded_update_column__  = None
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
    # automatic assigned columns
    __automatic_assigned_column__        = None
    __automatic_assigned_insert_column__ = None
    __automatic_assigned_update_column__ = None
    # privilege
    __allow_list__      = True
    __allow_show__      = True
    __allow_edit__      = True
    __allow_new__       = True
    __allow_trash__     = True
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
    
    def set_state_list(self):
        self._set_state('list')
        
    def _set_state(self, state):
        self.__state__ = state
    
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
            excluded_column_list_priorities = [self.__tabular_excluded_column__]
            virtual_column_list_priorities  = [self.__tabular_virtual_column__]
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
            excluded_column_list_priorities = [self.__detail_excluded_column__]
            virtual_column_list_priorities = [self.__detail_virtual_column__]
        # assign default value to column_list
        for config_list in column_list_priorities:
            if column_name in config_list and len(config_list[column_name]) > 0:
                column_list = config_list[column_name]
                break
        if len(column_list) == 0:
            obj = self._get_relation_class(column_name)()
            obj._set_state(state)
            column_list = obj._tabular_column_list
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
    def generated_style(self):
        if hasattr(self, '_generated_style'):
            return self._generated_style
        else:
            return ''
    
    @generated_style.setter
    def generated_style(self, val):
        self._generated_style = val
    
    @property
    def generated_script(self):
        if hasattr(self, '_generated_script'):
            return self._generated_script
        else:
            return ''
    
    @generated_script.setter
    def generated_script(self, val):
        self._generated_script = val
    
    @property
    def success(self):
        if hasattr(self, '_success'):
            return self._success
        else:
            return True
    
    @success.setter
    def success(self, val):
        self._success = val
    
    @classmethod
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
                    if isinstance(column_type, Date): # date
                        y,m,d = value.split('-')
                        y,m,d  = int(y), int(m), int(d)
                        value = datetime.date(y,m,d)
                    if isinstance(column_type, DateTime): # datetime
                        value = datetime.datetime(value)
                    if isinstance(column_type, Boolean):
                        if value == '0':
                            value = False
                        else:
                            value = True
                    setattr(self, column_name, value)
            elif column_name in self._get_relation_names():
                relation_metadata = self._get_relation_metadata(column_name)
                if relation_metadata.uselist:
                    ref_class = self._get_relation_class(column_name)
                    # one to many
                    old_id_list = []
                    deleted_list = []
                    relation_variable_list = []
                    index_list = []
                    record_count = 0
                    # by default bottle request doesn't automatically accept 
                    # POST with [] name
                    for variable_key in variable:
                        if hasattr(variable, 'getall') and variable_key[0:len(column_name)] == column_name and variable_key[-2:] == '[]':
                            # get list value
                            list_val = variable.getall(variable_key)
                            if len(list_val) > record_count:
                                record_count = len(list_val)
                                # make list of dictionary (as much as needed)
                                for i in xrange(record_count):
                                    relation_variable_list.append({})
                                    del(i)
                            new_variable_key = variable_key[len(column_name)+1:-2]
                            for i in xrange(record_count):
                                relation_variable_list[i][new_variable_key] = list_val[i]
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
                        if issubclass(ref_class, Ordered_DB_Model):
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
                        if issubclass(ref_class, Ordered_DB_Model):
                            ref_obj._index = index
                        if deleted:
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
        return self._get_actual_column_metadata(column_name).type
    
    def _save_detail(self, already_saved_object):
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, DB_Model):
                # one to many
                if relation_value not in already_saved_object:
                    relation_value.save(already_saved_object)
            elif isinstance(relation_value, list):
                # many to one
                for child in relation_value:
                    if isinstance(child, DB_Model):
                        if child not in already_saved_object:
                            child.save(already_saved_object)
    
    def _commit(self):
        # success or rollback
        if self.success:
            try:
                self.session.commit()
            except Exception, e:
                self.session.rollback()
                self.success = False
                logger.error('Database commit failed, ' + str(e))
        else:
            self.session.rollback()
            
    def save(self, already_saved_object = []):
        # is it insert or update?
        inserting = False
        if self._real_id is None:
            inserting = True
            # before insert
            self.before_insert()
            # insert
            if self.success:
                self.session.add(self)
        else:
            #before update
            self.before_update()
        self.before_save()
        # save
        self._commit()
        # generate id if not exists
        if self.id is None:
            self.generate_id()
        self._commit()
        # after insert, after update and after save
        if inserting:
            self.after_insert()
        else:
            self.after_update()
        self.after_save()
        # don't save the same object twice, it will make endless recursive
        already_saved_object.append(self)
        # also trigger save of relation
        self._save_detail(already_saved_object)
    
    def trash(self):
        self.before_trash()
        if self.success:
            self._trashed = True
        self._commit()
        self.after_trash()
        # also trash children
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, list):
                for child in relation_value:
                    if isinstance(child, DB_Model):
                        child.trash()
                        child.save()
    
    def untrash(self):
        self.before_untrash()
        if self.success:
            self._trashed = False
        self._commit()
        self.after_untrash()
        # also untrash children
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, list):
                for child in relation_value:
                    if isinstance(child, DB_Model):
                        child.untrash()
                        child.save()
    
    def delete(self):
        self.before_delete()
        if self.success:
            self.session.delete(self)
        self._commit()
        self.after_delete()
        # also delete children
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, list):
                for child in relation_value:
                    if isinstance(child, DB_Model):
                        child.trash()
                        child.delete()
    
    def generate_prefix_id(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime(self.__prefix_of_id__)
    
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
            newid = prefix + str(number+1).zfill(self.__digit_num_of_id__)
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
    
    def build_custom_label(self, column_name, **kwargs):
        '''
        Custom label if defined, override this if needed, but promise me 3 things:
        * add any additional css into self.generated_style
        * add any additional script into self.generated_script
        * return your HTML as string
        '''
        return None
    
    def build_custom_input(self, column_name, **kwargs):
        '''
        Custom input if defined, override this if needed, but promise me 3 things:
        * add any additional css into self.generated_style
        * add any additional script into self.generated_script
        * return your HTML as string
        '''
        return None
    
    def build_custom_representation(self, column_name, **kwargs):
        '''
        Custom representation if defined, override this if needed, but promise me 3 things:
        * add any additional css into self.generated_style
        * add any additional script into self.generated_script
        * return your HTML as string
        '''
        pass
    
    def build_custom_tabular_footer(self, column_name, **kwargs):
        '''
        Custom tabular last row if defined, override this if needed, but promise me 3 things:
        * add any additional css into self.generated_style
        * add any additional script into self.generated_script
        * return your HTML as string
        '''
        pass
    
    def build_label(self, column_name, **kwargs):
        ''' DON'T OVERRIDE THIS UNLESS YOU KNOW WHAT YOU DO
        This method is used to generate label
        '''
        # get custom_input if exists
        if hasattr(self, 'build_label_'+column_name):
            # call any "certain" custom_label
            function = getattr(self, 'build_label_'+column_name)
            custom_label = function(**kwargs)
        else:
            # call build_custom_label
            custom_label = self.build_custom_label(column_name, **kwargs)
        # return custom label or generate default one
        if custom_label is not None:
            return custom_label
        else:
            if column_name in self.__column_label__:
                return self.__column_label__[column_name]
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
    
    def build_input(self, column_name, **kwargs):
        ''' DON'T OVERRIDE THIS UNLESS YOU KNOW WHAT YOU DO
        This method is used to generate input
        '''
        # adjust kwargs
        input_attribute = kwargs.pop('input_attribute', {})
        if 'name' not in input_attribute:
            input_attribute['name'] = column_name
        if 'id' not in input_attribute and  input_attribute['name'][-2:] != '[]':
            input_attribute['id'] = 'field_' + column_name
        if 'class' not in input_attribute:
            input_attribute['class'] = []
        kwargs['input_attribute'] = input_attribute
        tabular = kwargs.pop('tabular', False)
        # get custom_input if exists
        if hasattr(self, 'build_input_'+column_name):
            # call any "certain" custom_input
            function = getattr(self, 'build_input_'+column_name)
            custom_input = function(**kwargs)
        else:
            # call build_custom_input
            custom_input = self.build_custom_input(column_name, **kwargs)
        # return custom_input or build the default inputs
        if custom_input is not None:
            return custom_input
        else:
            if hasattr(self, column_name):
                value = getattr(self, column_name)
            else:
                value = ''
            html = ''
            if column_name in self._get_relation_names():
                relation_metadata = self._get_relation_metadata(column_name)
                if relation_metadata.uselist:
                    # one to many
                    ref_class = self._get_relation_class(column_name)
                    ref_obj = ref_class()
                    # determine if the model is ordered
                    is_ordered = isinstance(ref_obj, Ordered_DB_Model)
                    # column name
                    if column_name in self.__detail_column_label__:
                        custom_label = self.__detail_column_label__[column_name]
                    else:
                        custom_label = {}
                    ref_obj.generate_tabular_label(state = 'form', shown_column = self._get_detail_column_list(column_name), custom_label = custom_label)
                    if len(getattr(self, column_name)) == 0:
                        div_empty_style = ''
                        table_style = 'style="display:none;"'
                        div_control_class = ''
                    else:
                        div_empty_style = 'style="display:none;"'
                        table_style = ''
                        div_control_class = 'pull-right'
                    # div empty
                    input_element  = '<div id="_div_empty_'+column_name+'" '+div_empty_style+'>No data</div>'
                    # div control
                    input_element += '<div id="_div_control_'+column_name+'" class="'+div_control_class+'">'
                    input_element += '<a id="_' + column_name + '_add" class="btn btn-default _new_row" href="#">'
                    input_element += '<i class="glyphicon glyphicon-plus"></i> New ' + self.build_label(column_name)
                    input_element += '</a>'
                    input_element += '</div>'
                    # table
                    input_element += '<table id="_table_'+column_name+'" class="table" '+table_style+'>'
                    input_element += '<thead>'
                    input_element += '<tr>'
                    input_element += ref_obj.generated_html
                    if is_ordered:
                        input_element += '<th>Order</th>'
                    input_element += '<th>Delete</th>'
                    input_element += '</tr>'
                    input_element += '</thead>'
                    # body
                    input_element += '<tbody id="_' + column_name + '_tbody">'
                    row_index = 0
                    for child in getattr(self, column_name):
                        child.generate_tabular_input(state = 'form', shown_column = self._get_detail_column_list(column_name), parent_column_name = column_name)
                        input_element += '<tr>'
                        input_element += child.generated_html
                        if is_ordered:
                            input_element += '<td>'
                            input_element += '<input class="_'+column_name+'_index" id="_'+column_name+'_index_'+str(row_index)+'" type="hidden" name="_'+column_name+'_index[]" value="'+str(row_index)+'" />'
                            input_element += '<a class="_'+column_name+'_up" row-index="'+str(row_index)+'" href="#"><i class="glyphicon glyphicon glyphicon-arrow-up"></i></a>'
                            input_element += '<a class="_'+column_name+'_down" row-index="'+str(row_index)+'" href="#"><i class="glyphicon glyphicon glyphicon-arrow-down"></i></a>'
                            input_element += '</td>'
                        input_element += '<td>'
                        input_element += '    <input type="hidden" name="_' + column_name + '_id[]" value="' + str(child.id) + '" />'
                        input_element += '    <input class="deleted" type="hidden" name="_' + column_name + '_delete[]" value="0" />'
                        input_element += '    <label><input type="checkbox" class="_' + column_name + '_delete"></label>'
                        input_element += '</td>'
                        input_element += '</tr>'
                        row_index +=1
                    input_element += '</tbody>'
                    input_element += '</table>'
                    # what should be added when add row clicked
                    ref_obj.generate_tabular_input(state = 'form', shown_column = self._get_detail_column_list(column_name), parent_column_name = column_name)
                    new_row  = '\'<tr>'
                    new_row += ref_obj.generated_html
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
                    script  = '<script type="text/javascript">'
                    if is_ordered:
                        script += 'var ' + last_index_varname + ' = ' + str(row_index) + ';'
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
                    script += '</script>'
                    self.generated_script += script
                    
                else:
                    # many to one
                    ref_class = self._get_relation_class(column_name)
                    option_obj = ref_class.get()
                    option_count = ref_class.count()
                    input_element = ''
                    if option_count == 0:
                        input_element += 'No option available'
                    elif option_count <= 3 and not tabular:
                        xs_width = sm_width = str(12/option_count)
                        md_width = lg_width = str(9/option_count)
                        for obj in option_obj:
                            input_attribute['type'] = 'radio'
                            input_attribute['value'] = obj.id
                            if value == obj:
                                input_attribute['checked'] = 'checked'
                            else:
                                input_attribute.pop('checked', None)
                            input_element += '<div class="col-xs-' + xs_width + ' col-sm-' + sm_width + ' col-md-' + md_width + ' col-lg-' + lg_width+ '">'
                            input_element += '<label><input ' + self._encode_input_attribute(input_attribute) + ' /> ' + obj.quick_preview() + '</label>'
                            input_element += '</div>'
                    else:
                        input_attribute['class'].append('form-control')
                        input_element += '<select ' + self._encode_input_attribute(input_attribute) + '>'
                        input_element += '<option value="">None</option>'
                        for obj in option_obj:
                            if value == obj:
                                selected = 'selected'
                            else:
                                selected = ''
                            input_element += '<option ' + selected + ' value="' + obj.id + '">' + obj.quick_preview() + '</option>'
                        input_element += '</select>'
            else:
                if value is None:
                    value = ''
                label = self.build_label(column_name, **kwargs)
                # check type
                column_type = self._get_actual_column_type(column_name)
                if isinstance(column_type, Boolean):
                    input_attribute['type'] = 'checkbox'
                    input_attribute['value'] = '1'
                    if value:
                        input_attribute['checked'] = 'checked'
                    else:
                        input_attribute.pop('checked', None)
                    input_element = '<input type="hidden" name="' + input_attribute['name'] + '" value="0" />'
                    input_element += '<input ' + self._encode_input_attribute(input_attribute) + ' />'
                else:
                    value = str(value)
                    # build additional_class
                    if isinstance(column_type, Date):
                        input_attribute['class'].append('_date-input')
                    elif isinstance(column_type, Integer):
                        input_attribute['class'].append('_integer-input')
                        if value == '':
                            value = '0'
                    input_attribute['type'] = 'text'
                    input_attribute['value'] = value
                    input_attribute['placeholder'] = label
                    input_attribute['class'].append('form-control')
                    input_element = '<input ' + self._encode_input_attribute(input_attribute) + ' />'
            html += input_element
            return html
    
    def build_labeled_input(self, column_name, **kwargs):
        label = self.build_label(column_name, **kwargs)
        html  = '<div class="form-group">'
        html += '<label for="field_' + column_name + '" class="col-xs-12 col-sm-12 col-md-3 col-lg-3 control-label">' + label + '</label>'
        html += '<div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">'
        html += self.build_input(column_name, **kwargs)
        html += '</div>'
        html += '</div>'
        return html
    
    def build_representation(self, column_name, **kwargs):
        ''' DON'T OVERRIDE THIS UNLESS YOU KNOW WHAT YOU DO
        This method is used to generate representation
        '''
        # get custom_input if exists
        if hasattr(self, 'build_representation_'+column_name):
            # call any "certain" custom_representation
            function = getattr(self, 'build_representation_'+column_name)
            custom_representation = function(**kwargs)
        else:
            # call build_custom_representation
            custom_representation = self.build_custom_representation(column_name, **kwargs)
        # return custom representation or generate default one
        if custom_representation is not None:
            return custom_representation
        else:
            if hasattr(self, column_name):
                value = getattr(self, column_name)
            else:
                value = ''
            # if it is relation, retrieve it
            if column_name in self._get_relation_names():
                relation_metadata = self._get_relation_metadata(column_name)
                if relation_metadata.uselist:
                    if isinstance(value, list) and len(value)>0:
                        children = getattr(self,column_name)
                        # generate new value
                        '''
                        value = '<ul>'
                        for child in children:
                            value += '<li>' + child.quick_preview() + '</li>'
                        value += '<ul>'
                        '''
                        
                        # table
                        ref_obj = self._get_relation_class(column_name)()
                        ref_obj = self._get_relation_class(column_name)()
                        if column_name in self.__detail_column_label__:
                            custom_label = self.__detail_column_label__[column_name]
                        else:
                            custom_label = {}
                        ref_obj.generate_tabular_label(state = 'view', shown_column = self._get_detail_column_list(column_name), custom_label = custom_label)
                        value  = '<table class="table">'
                        value += '<thead><tr>' + ref_obj.generated_html + '</tr></thead>'
                        value += '<tbody>'
                        for child in children:
                            child.generate_tabular_representation(state = 'view', shown_column = self._get_detail_column_list(column_name))
                            value += '<tr>'
                            value += child.generated_html
                            value += '</tr>'
                        value += '</tbody>'
                        footer = self.build_custom_tabular_footer(column_name, state = 'view')
                        if footer is not None:
                            value += '<tfoot>'
                            value += footer
                            value += '</tfoot>'
                        value += '</table>'
                # lookup value
                elif isinstance(value, DB_Model):
                    obj = getattr(self, column_name)
                    value = obj.quick_preview()
            # None or empty children
            if value is None or (isinstance(value,list) and len(value)==0):
                value = 'Not available'
            value = str(value)
            return value
    
    def build_labeled_representation(self, column_name, **kwargs):
        label = self.build_label(column_name, **kwargs)
        html  = '<div class="form-group row container col-xs-12 col-sm-12 col-md-12 col-lg-12">'
        html += '<label class="col-xs-12 col-sm-12 col-md-3 col-lg-3 control-label">' + label + '</label>'
        html += '<div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">'
        html += self.build_representation(column_name, **kwargs)
        html += '</div>'
        html += '</div>'
        return html
    
    def reset_generated(self):
        self._generated_html = ''
        self._generated_script = ''
        self._generated_css = ''
    
    def _include_default_resource(self):
        base_url = base_url()
        self._generated_script += asset.JQUI_BOOTSTRAP_SCRIPT
        self._generated_script += asset.KOKORO_CRUD_SCRIPT
        self._generated_css += asset.JQUI_BOOTSTRAP_STYLE
        self._generated_css += asset.KOKORO_CRUD_STYLE

    def quick_preview(self):
        '''
        Quick preview of record, override this
        '''
        column_list = self._column_list
        if len(column_list) >1:
            return getattr(self, column_list[1])
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
            html += '<th>' + label + '</th>'
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
            html += '<td>' + self.build_representation(column_name) + '</td>'
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
            html += '<td>' + self.build_input(column_name, input_attribute = input_attribute, tabular = True) + '</td>'
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
        html = '<div class="row container">'
        for column_name in self._column_list:
            html += self.build_labeled_representation(column_name)
        html += '</div>'
        self.generated_html = html

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