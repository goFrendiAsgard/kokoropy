from sqlalchemy import create_engine, Column, func, BIGINT, BigInteger, BINARY, Binary,\
    BOOLEAN, Boolean, DATE, Date, DATETIME, DateTime, FLOAT, Float,\
    INTEGER, Integer, VARCHAR, String, TEXT, Text, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from alembic.migration import MigrationContext
from alembic.operations import Operations
import datetime, time, json
from kokoropy import Fore, Back, base_url
import asset

# initialize logger
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    __virtual_showncolumn__ = None
    __virtual_formcolumn__ = None
    __virtual_insertformcolumn__ = None
    __virtual_updateformcolumn__ = None
    __excluded_showncolumn__ = None
    __excluded_formcolumn__ = None
    __excluded_insertformcolumn__ = None
    __excluded_updateformcolumn__ = None
    __tabular_showncolumn__ = None
    __tabular_formcolumn__ = None
    __assign_column__ = None
        
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    @property
    def _shown_column(self):
        if self.__showncolumn__ is None:
            self.__showncolumn__ = []
            for column_name in self._get_column_names():
                if column_name in ['_real_id', '_created_at', '_updated_at', '_trashed'] or column_name.split('_')[0] == 'fk':
                    continue
                self.__showncolumn__.append(column_name)
            for relation_name in self._get_relation_names():
                self.__showncolumn__.append(relation_name)
        # remove unshown_column
        if self.__excluded_showncolumn__ is not None:
            for unshown_column in self.__excluded_showncolumn__:
                if unshown_column in self.__showncolumn__:
                    self.__showncolumn__.remove(unshown_column)
            self.__excluded_showncolumn__ = None
        # add virtual column
        if self.__virtual_showncolumn__ is not None:
            for virtual_column in self.__virtual_showncolumn__:
                self.__showncolumn__.append(virtual_column)
        return self.__showncolumn__
    
    @property
    def _form_column(self):
        if self.__formcolumn__ is None:
            form_column = self._shown_column
        else:
            form_column = self.__formcolumn__
        # remove excluded column
        if self.__excluded_formcolumn__ is not None:
            for excluded_column in self.__excluded_formcolumn__:
                if excluded_column in form_column:
                    form_column.remove(excluded_column)
            self.__excluded_formcolumn__ = None
        # add virtual column
        if self.__virtual_formcolumn__ is not None:
            for virtual_column in self.__virtual_formcolumn__:
                self.__showncolumn__.append(virtual_column)
        return form_column
    
    @property
    def _insert_form_column(self):
        if self.__insertformcolumn__ is None:
            form_column = self._form_column
        else:
            form_column = self.__insertformcolumn__
        # remove excluded column
        if self.__excluded_insertformcolumn__ is not None:
            for excluded_column in self.__excluded_insertformcolumn__:
                if excluded_column in form_column:
                    form_column.remove(excluded_column)
            self.__excluded_insertformcolumn__ = None
        # add virtual column
        if self.__virtual_insertformcolumn__ is not None:
            for virtual_column in self.__virtual_insertformcolumn__:
                self.__showncolumn__.append(virtual_column)
        return form_column
    
    @property
    def _update_form_column(self):
        if self.__updateformcolumn__ is None:
            form_column = self._form_column
        else:
            form_column = self.__updateformcolumn__
        # remove excluded column
        if self.__excluded_updateformcolumn__ is not None:
            for excluded_column in self.__excluded_updateformcolumn__:
                if excluded_column in form_column:
                    form_column.remove(excluded_column)
            self.__excluded_updateformcolumn__ = None
        # add virtual column
        if self.__virtual_showncolumn__ is not None:
            for virtual_column in self.__virtual_updateformcolumn__:
                self.__showncolumn__.append(virtual_column)
        return form_column
    
    @property
    def _assign_column(self):
        if self.__assign_column__ is None:
            assign_column = self.__assign_column__
        else:
            assign_column = self._form_column
        return assign_column
    
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
    
    def assign(self, variable):
        for column_name in self._get_column_names():
            if column_name in self._assign_column:
                column_type = self._get_column_type(column_name)
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
        for relation_name in self._get_relation_names():
            if relation_name in self._assign_column:
                relation_metadata = self._get_relation_metadata(relation_name)
                if relation_metadata.uselist:
                    # one to many
                    old_id_list = []
                    deleted_list = []
                    relation_variable_list = []
                    record_count = 0
                    # by default bottle request doesn't automatically accept 
                    # POST with [] name
                    for variable_key in variable:
                        if hasattr(variable, 'getall') and variable_key[0:len(relation_name)] == relation_name and variable_key[-2:] == '[]':
                            # get list value
                            list_val = variable.getall(variable_key)
                            if len(list_val) > record_count:
                                record_count = len(list_val)
                                # make list of dictionary (as much as needed)
                                for i in xrange(record_count):
                                    relation_variable_list.append({})
                                    del(i)
                            new_variable_key = variable_key[len(relation_name)+1:-2]
                            print new_variable_key, list_val
                            for i in xrange(record_count):
                                relation_variable_list[i][new_variable_key] = list_val[i]
                    if hasattr(variable, 'getall'):
                        old_id_list = variable.getall('_' + relation_name + '_id[]')
                        deleted_list = variable.getall('_' + relation_name + '_delete[]')
                    ref_class = self._get_relation_class(relation_name)
                    # get relation
                    relation_value = self._get_relation_value(relation_name)
                    for i in xrange(record_count):
                        old_id = old_id_list[i]
                        deleted = deleted_list[i] == "1"
                        relation_variable = relation_variable_list[i]
                        ref_obj = None
                        for child in relation_value:
                            if isinstance(child, Model):
                                if child.id == old_id:
                                    ref_obj = child
                                    ref_obj.assign(relation_variable)
                                    break
                        if ref_obj is None:
                            ref_obj = ref_class()
                            ref_obj.assign(relation_variable)
                            getattr(self, relation_name).append(ref_obj)
                        if deleted:
                            getattr(self, relation_name).remove(ref_obj)
                else:
                    # many to one
                    if relation_name in variable and variable[relation_name] != '':
                        value = variable[relation_name]
                        if value != '':
                            ref_class = self._get_relation_class(relation_name)
                            value = ref_class.find(value)
                        setattr(self, relation_name, value)
    
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
        return self.__mapper__.relationships._data
    
    def _get_relation_metadata(self, relation_name):
        return getattr(self.__mapper__.relationships, relation_name)
    
    def _get_relation_class(self, relation_name):
        return getattr(self.__class__, relation_name).property.mapper.class_
    
    def _get_relation_value(self, relation_name):
        return getattr(self, relation_name)
    
    def _get_column_names(self):
        if not hasattr(self, '__column_names'):
            self.__column_names = []
            for column in self.__table__.columns:
                self.__column_names.append(column.name)
        return self.__column_names
    
    def _get_column_metadata(self, column_name):
        if not hasattr(self, '__column'):
            self.__column = {}
            for column in self.__table__.columns:
                self.__column[column.name] = column
        return self.__column[column_name]
    
    def _get_column_type(self, column_name):
        return self._get_column_metadata(column_name).type
    
    def _save_relation_value(self):
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, Model):
                # one to many
                relation_value.save()
            elif isinstance(relation_value, list):
                # many to one
                for child in relation_value:
                    if isinstance(child, Model):
                        child.save()
    
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
        self._save_relation_value()
    
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
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, list):
                for child in relation_value:
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
        for relation_name in self._get_relation_names():
            relation_value = self._get_relation_value(relation_name)
            if isinstance(relation_value, list):
                for child in relation_value:
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
        # get column value
        for column_name in self._get_column_names():
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
    
    def build_label(self, column_name, **kwargs):
        custom_label = self.build_custom_label(column_name, **kwargs)
        if custom_label is not None:
            return custom_label
        else:
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
        '''
            * input_attribute
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
        # call build_custom_input
        custom_input = self.build_custom_input(column_name, **kwargs)
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
                    input_element = 'One to Many'
                    ref_obj = self._get_relation_class(column_name)()
                    ref_obj.generate_tabular_label(state = 'form')
                    input_element  = '<div class="pull-right">'
                    input_element += '<a id="_' + column_name + '_add" class="btn btn-default _new_row" href="#">'
                    input_element += '<i class="glyphicon glyphicon-plus"></i> New ' + self.build_label(column_name)
                    input_element += '</a>'
                    input_element += '</div>'
                    input_element += '<table class="table">'
                    input_element += '<thead>'
                    input_element += '<tr>'
                    input_element += ref_obj.generated_html
                    input_element += '<th>Delete</th>'
                    input_element += '</tr>'
                    input_element += '</thead>'
                    # TODO : apply clean "delete" scenario
                    # what should be added when add row clicked
                    ref_obj.generate_tabular_input(state = 'form', parent_column_name = column_name)
                    new_row  = '<tr>'
                    new_row += ref_obj.generated_html
                    # delete column
                    new_row += '<td>'
                    new_row += '    <input type="hidden" name="_' + column_name + '_id[]" value="" />'
                    new_row += '    <input class="deleted" type="hidden" name="_' + column_name + '_delete[]" value="0" />'
                    new_row += '    <label><input type="checkbox" class="_' + column_name + '_delete"></label>'
                    new_row += '</td>'
                    new_row += '</tr>'
                    script  = '<script type="text/javascript">'
                    script += '$("._' + column_name + '_delete").live("click", function(event){'
                    script += '    var input = $(this).parent().parent().children(".deleted");'
                    script += '    if($(this).prop("checked")){'
                    script += '        input.val("1");'
                    script += '    }else{'
                    script += '        input.val("0");'
                    script += '    }'
                    script += '});'
                    script += '$("#_' + column_name + '_add").click(function(event){'
                    script += '    $("#_' + column_name + '_tbody").append(\'' + new_row + '\');'
                    script += '    event.preventDefault();'
                    script += '});'
                    script += '</script>'
                    self.generated_script += script
                    # body
                    input_element += '<tbody id="_' + column_name + '_tbody">'
                    for child in getattr(self, column_name):
                        child.generate_tabular_input(state = 'form', parent_column_name = column_name)
                        input_element += '<tr>'
                        input_element += child.generated_html
                        input_element += '<td>'
                        input_element += '    <input type="hidden" name="_' + column_name + '_id[]" value="' + str(child.id) + '" />'
                        input_element += '    <input class="deleted" type="hidden" name="_' + column_name + '_delete[]" value="0" />'
                        input_element += '    <label><input type="checkbox" class="_' + column_name + '_delete"></label>'
                        input_element += '</td>'
                        input_element += '</tr>'
                    input_element += '</tbody>'
                    input_element += '</table>'
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
                column_type = self._get_column_type(column_name)
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
        custom_representation = self.build_custom_representation(column_name, **kwargs)
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
                        ref_obj.generate_tabular_label()
                        value  = '<table class="table">'
                        value += '<thead><tr>' + ref_obj.generated_html + '</tr></thead>'
                        value += '<tbody>'
                        for child in children:
                            child.generate_tabular_representation()
                            value += '<tr>'
                            value += child.generated_html
                            value += '</tr>'
                        value += '</tbody>'
                        value += '</table>'
                # lookup value
                elif isinstance(value, Model):
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
    
    def include_resource(self):
        base_url = base_url()
        self._generated_script += asset.default_script()
        self._generated_css += asset.default_style()

    def quick_preview(self):
        '''
        Quick preview of record, override this
        '''
        return self.id
    
    def _get_tabular_column_names_by_state(self, state = None):
        '''
        state: "view" or "form"
        '''
        if state is None or state == 'list' or state == 'view':
            if self.__tabular_showncolumn__ is not None:
                column_names = self.__tabular_showncolumn__
            else:
                column_names = self._shown_column
        elif state == 'form' or state == 'new' or state == 'create' or state == 'insert' or state == 'add' or state == 'edit' or state == 'update':
            if self.__tabular_formcolumn__ is not None:
                column_names = self.__tabular_formcolumn__
            else:
                column_names = self._form_column
        return column_names
    
    def generate_tabular_label(self, state = None, include_resource = False, **kwargs):
        # prepare resource
        self.reset_generated()
        if include_resource:
            self.include_resource()
        # create html
        html  = ''
        for column_name in self._get_tabular_column_names_by_state(state):
            if column_name in self._get_relation_names() and self._get_relation_class(column_name) == self.__class__:
                continue
            html += '<th>' + self.build_label(column_name) + '</th>'
        self.generated_html = html
    
    def generate_tabular_representation(self, state = None, include_resource = False, **kwargs):
        # prepare resource
        self.reset_generated()
        if include_resource:
            self.include_resource()
        # create html
        html  = ''
        for column_name in self._get_tabular_column_names_by_state(state):
            if column_name in self._get_relation_names() and self._get_relation_class(column_name) == self.__class__:
                continue
            html += '<td>' + self.build_representation(column_name) + '</td>'
        self.generated_html = html
    
    def generate_tabular_input(self, state = None, include_resource = False, **kwargs):
        # prepare resource
        self.reset_generated()
        if include_resource:
            self.include_resource()
        # create html
        html  = ''
        parent_column_name = kwargs.pop('parent_column_name', '')
        for column_name in self._get_tabular_column_names_by_state(state):
            if column_name in self._get_relation_names() and self._get_relation_class(column_name) == self.__class__:
                continue
            input_name = parent_column_name + '_' + column_name + '[]' if parent_column_name != '' else column_name+'[]'
            input_attribute = {'name': input_name}
            html += '<td>' + self.build_input(column_name, input_attribute = input_attribute, tabular = True) + '</td>'
        self.generated_html = html
    
    def generate_input_view(self, state = None, include_resource = False, **kwargs):
        '''
        Input view of record
        '''
        # prepare resource
        self.reset_generated()
        if include_resource:
            self.include_resource()
        # determine which input column is used
        if state is None:
            input_column = self._form_column
        if state == 'new' or state == 'create' or state == 'insert' or state == 'add':
            input_column = self._insert_form_column
        elif state == 'edit' or state == 'update':
            input_column = self._update_form_column
        # build html
        html = ''
        for column_name in input_column:
            html += self.build_labeled_input(column_name)
        self.generated_html = html
        
    
    def generate_detail_view(self, include_resource = False, **kwargs):
        '''
        Detail view of record, override this with care
        '''
        # prepare resource
        self.reset_generated()
        if include_resource:
            self.include_resource()
        # build html
        html = '<div class="row container">'
        for column_name in self._shown_column:
            html += self.build_labeled_representation(column_name)
        html += '</div>'        
        self.generated_html = html

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