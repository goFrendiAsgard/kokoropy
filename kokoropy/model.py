from sqlalchemy import create_engine, Column, func, BIGINT, BigInteger, BINARY, Binary,\
    BOOLEAN, Boolean, DATE, Date, DATETIME, DateTime, FLOAT, Float,\
    INTEGER, Integer, VARCHAR, String, TEXT, Text, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from alembic.migration import MigrationContext
from alembic.operations import Operations
import datetime, time, json
from kokoropy import Fore, Back

# create Base
Base = declarative_base()
        
class Model(Base):
    '''
    Model
    '''
    _real_id = Column(Integer, primary_key=True)
    _trashed = Column(Boolean, default=False)
    _created_at = Column(DateTime, default=func.now())
    _updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    id = Column(String(35), unique=True)
    
    __abstract__ = True
    __connectionstring__ = ''
    __echo__ = True
    __prefixid__ = '%Y%m%d-'
    __digitid__ = 3
    __showncolumn__ = None
    __formcolumn__ = None
    __insertformcolumn__ = None
    __updateformcolumn__ = None
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    @property
    def _shown_column(self):
        if self.__showncolumn__ is None:
            self.__showncolumn__ = []
            for column in self.__table__.columns:
                column = column.name
                if column in ['_real_id', '_created_at', '_updated_at', '_trashed', 'id'] or column.split('_')[0] == 'fk':
                    continue
                self.__showncolumn__.append(column)
            for relation_name in self._get_relation_name():
                self.__showncolumn__.append(relation_name)
        return self.__showncolumn__
    
    @property
    def _form_column(self):
        if self.__formcolumn__ is None:
            return self._shown_column
        else:
            return self.__formcolumn__
    
    @property
    def _insert_form_column(self):
        if self.__insertformcolumn__ is None:
            return self._form_column
        else:
            return self.__insertformcolumn__
    
    @property
    def _update_form_column(self):
        if self.__insertformcolumn__ is None:
            return self._form_column
        else:
            return self.__insertformcolumn__
    
    @property
    def engine(self):
        if hasattr(self, '__session__'):
            self.__engine__ = self.session.bind
        elif not hasattr(self, '__engine__'):
            self.__engine__ = create_engine(self.__connectionstring__, echo=self.__echo__)
        return self.__engine__
    
    @property
    def session(self):
        if not hasattr(self, '__session__'):
            if not hasattr(self, '__engine__'):
                self.__engine__ = create_engine(self.__connectionstring__, echo=self.__echo__)
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
            Model.get(Model.name=="whatever", limit=1000, offset=0, include_trashed=True, as_json=True, include_relation=True)
        '''
        # get kwargs parameters
        limit = kwargs.pop('limit', 1000)
        offset = kwargs.pop('offset', 0)
        include_trashed = kwargs.pop('include_trashed', False)
        as_json = kwargs.pop('as_json', False)
        include_relation = kwargs.pop('include_relation', False)
        # get / make session if not exists
        if hasattr(cls,'__session__ '):
            session = cls.__session__
        else:
            obj = cls()
            session = obj.session
        query = session.query(cls)
        if include_trashed == False:
            query = query.filter(cls._trashed == False)
        # run the query
        result = query.filter(*criterion).limit(limit).offset(offset).all()
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
        include_relation = kwargs.pop('include_relation', False)
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
    def find(cls, id_value):
        result = cls.get(cls.id == id_value)
        if len(result)>0:
            return result[0]
    
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
    
    def _get_relation_name(self):
        return self.__mapper__.relationships._data
    
    def _get_relation(self, relation_name):
        return getattr(self, relation_name)
    
    def _save_relation(self):
        for relation_name in self._get_relation_name():
            relation = self._get_relation(relation_name)
            if isinstance(relation, Model):
                relation.save()
            elif isinstance(relation, list):
                for child in relation:
                    if isinstance(child, Model):
                        child.save()
    
    def _commit(self):
        # success or rollback
        if self.success:
            self.session.commit()
        else:
            self.session.rollback()
            
    def save(self):
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
        # also trigger save of relation
        self._save_relation()
    
    def trash(self):
        self.before_trash()
        if self.success:
            self._trashed = True
        self._commit()
        self.after_trash()
        # also trash children
        for relation_name in self._get_relation_name():
            relation = self._get_relation(relation_name)
            if isinstance(relation, list):
                for child in relation:
                    if isinstance(child, Model):
                        child.trash()
                        child.save()
    
    def untrash(self):
        self.before_untrash()
        if self.success:
            self._trashed = False
        self._commit()
        self.after_untrash()
        # also untrash children
        for relation_name in self._get_relation_name():
            relation = self._get_relation(relation_name)
            if isinstance(relation, list):
                for child in relation:
                    if isinstance(child, Model):
                        child.untrash()
                        child.save()
    
    def delete(self):
        self.before_delete()
        if self.success:
            self.session.delete(self)
        self._commit()
        self.after_delete()
        # also delete children
        for relation_name in self._get_relation_name():
            relation = self._get_relation(relation_name)
            if isinstance(relation, list):
                for child in relation:
                    if isinstance(child, Model):
                        child.trash()
                        child.delete()
    
    def generate_prefix_id(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime(self.__prefixid__)
    
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
            newid = prefix + str(number+1).zfill(self.__digitid__)
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
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if isoformat and hasattr(val, 'isoformat'):
                val = val.isoformat()
            dictionary[column.name] = val
        # also include_relation
        if include_relation:
            kwargs = {'isoformat': isoformat}
            # also add relation to dictionary
            for relation_name in self._get_relation_name():
                relation = self._get_relation(relation_name)
                if isinstance(relation, Model):
                    dictionary[relation_name] = relation.to_dict(**kwargs)
                elif isinstance(relation, list):
                    dictionary[relation_name] = []
                    for child in relation:
                        if isinstance(child, Model):
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
    
    def build_column(self, column_name):
        '''
        Custom column if defined, override this if needed
        '''
        return None
    
    def build_input(self, column_name):
        '''
        Custom input if defined, override this if needed
        '''
        return None
    
    def quick_preview(self):
        '''
        Quick preview of record, override this
        '''
        return self.id
    
    def input_view(self, state = None):
        '''
        Input view of record
        '''
        dictionary = self.to_dict(include_relation = True)
        # determine which input column is used
        if state is None:
            input_column = self._form_column
        if state == 'new' or state == 'create' or state == 'insert' or state == 'add':
            input_column = self._insert_form_column
        elif state == 'edit' or state == 'update':
            input_column = self._update_form_column
        # build html
        html = ''
        relation_properties = self.__mapper__.relationships._data
        for key in input_column:
            label = key.replace('_', ' ').title()
            html += '<div class="form-group">'
            html += '<label for="field_' + key + '" class="col-xs-12 col-sm-12 col-md-3 col-lg-3 control-label">' + label + '</label>'
            html += '<div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">'
            custom_input = self.build_input(key)
            if custom_input is not None:
                input_element = custom_input
            else:
                value = getattr(self, key)
                if key in relation_properties:
                    relation = relation_properties[key]
                    ref_class = getattr(self.__class__, key).property.mapper.class_
                    if relation.uselist:
                        # one to many
                        input_element = 'One to Many'
                    else:
                        # many to one
                        option_obj = ref_class.get()
                        option_count = ref_class.count()
                        input_element = ''
                        if option_count == 0:
                            input_element += 'No option available'
                        elif option_count <= 3:
                            xs_width = sm_width = str(12/option_count)
                            md_width = lg_width = str(9/option_count)
                            for obj in option_obj:
                                if value == obj:
                                    selected = 'selected'
                                else:
                                    selected = ''
                                input_element += '<div class="col-xs-' + xs_width + ' col-sm-' + sm_width + ' col-md-' + md_width + ' col-lg-' + lg_width+ '">'
                                input_element += '<label><input type="radio" ' + selected + ' name ="' + key + '" value="' + obj.id + '"/> ' + obj.quick_preview() + '</label>'
                                input_element += '</div>'
                        else:
                            input_element += '<select class="form-control" id="field_' + key + '" name ="' + key + '">'
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
                    else:
                        value = str(value)
                    input_element = '<input type="text" class="form-control" id="field_' + key + '" name="' + key + '" placeholder="' + label + '" value="' + value + '">'
            html += input_element
            html += '</div>'
            html += '</div>'
        
        return html
        
    
    def detail_view(self):
        '''
        Detail view of record, override this with care
        '''
        dictionary = self.to_dict(include_relation = True)
        # build html
        html = '<div class="row container">'
        html += '<div class="row container col-xs-12 col-sm-12 col-md-12 col-lg-12">'
        html += '<h3>' + str(self.id) + '</h3>'
        html += '</div>'
        for key in self._shown_column:
            # row
            html += '<div class="row container col-xs-12 col-sm-12 col-md-12 col-lg-12">'
            label = key.replace('_', ' ').title()
            
            custom_value = self.build_column(key)
            if custom_value is not None:
                value = custom_value
            else:
                if key in dictionary:
                    value = dictionary[key]
                else:
                    value = None
            # pre-process
            if isinstance(value, list) and len(value)>0:
                children = getattr(self,key)
                # generate new value
                value = '<ul>'
                for child in children:
                    value += '<li>' + child.quick_preview() + '</li>'
                value += '<ul>'
            label_class = 'col-xs-12 col-sm-12 col-md-3 col-lg-3'
            content_class = 'col-xs-12 col-sm-12 col-md-9 col-lg-9'
            # lookup value
            if isinstance(value, dict):
                    obj = getattr(self, key)
                    value = obj.quick_preview()
            # None or empty children
            if value is None or (isinstance(value,list) and len(value)==0):
                value = 'Not available'
            # label
            html += '<div class="' + label_class + '">'
            html += '<label>' + str(label) + '</label>'
            html += '</div>'
            # value
            html += '<div class="' + content_class + '">'
            html += str(value)
            html += '</div>'
            # end of row
            html += '</div>'
        html += '</div>'        
        return html

def auto_migrate(engine):
    print('    %s%s WARNING %s%s%s : You are using auto_migrate()\n    Note that not all operation supported. Be prepared to do things manually.\n    Using auto_migration in production mode is not recommended.%s%s' %(Fore.BLACK, Back.GREEN, Fore.RESET, Back.RESET, Fore.GREEN, Fore.RESET, Fore.MAGENTA))
    # make model_meta & db_meta
    Model.metadata.create_all(bind=engine)
    model_meta = Model.metadata
    db_meta = MetaData()
    db_meta.reflect(bind=engine)
    # create db session & alembic operation
    db_session = scoped_session(sessionmaker(bind=engine))
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
        db_column_list = None
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
            except:
                print('    Fail to make table: %s, please add it manually' % (model_table_name))
        else:
            db_table = db_meta.tables[model_table_name]
        for model_column in model_table.columns:
            # don't create or alter default columns
            if model_column.name in default_column_names:
                continue
            # get model_column properties
            model_column_kwargs = {}
            for prop in column_properties:
                model_column_kwargs[prop] = getattr(model_column, prop)
            # make model_column with alembic if necessary
            if model_column.name not in db_meta.tables[model_table_name].columns:
                try:
                    op.add_column(model_table_name, Column(model_column.name, model_column.type, **model_column_kwargs))
                except:
                    print('    Fail to make column %s.%s, please add it manually' % (model_table_name, model_column.name))
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
                    except:
                        print('    Fail to alter column %s.%s, please alter it manually.\n      Old type: %s, new type: %s' % (model_table_name, model_column.name, str(db_column.type), str(model_column.type)))
    print(Fore.RESET)