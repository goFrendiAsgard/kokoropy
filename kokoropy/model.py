from sqlalchemy import create_engine, Column, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import datetime, time, json
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
    id = Column(String, unique=True)
    
    __abstract__ = True
    __connectionstring__ = ''
    __echo__ = True
    __prefixid__ = '%Y%m%d-'
    __digitid__ = 3
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
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