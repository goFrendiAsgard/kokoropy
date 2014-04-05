from sqlalchemy import create_engine, Column, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime, time, json
# create Base
Base = declarative_base()

class Mixin(object):
    '''
    Don't use these names as field name:
    * engine
    * session
    * error_message
    * success
    * id
    * get
    * find
    * before_save
    * before_insert
    * before_update
    * before_trash
    * before_untrash
    * before_delete
    * save
    * trash
    * untrash
    * delete
    * generate_prefix_id
    * generate_id
    * to_dict
    * to_json
    '''
    _real_id = Column(Integer, primary_key=True)
    _trashed = Column(Boolean, default=False)
    _created_at = Column(DateTime, default=func.now())
    _updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    id = Column(String, unique=True, default=func.current_timestamp())
    
    __connectionstring__ = ''
    __echo__ = True
    __prefixid__ = '%Y%m%d-'
    __digitid__ = 3
    
    
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
        cls_name = cls.__name__
        obj = cls()
        #obj._init_db()
        trashed_property = cls_name + '._trashed'
        # define default value for limit and offset
        limit = kwargs.pop('limit', 1000)
        offset = kwargs.pop('offset', 0)
        # make query, by default trashed = False
        trashed = kwargs.pop(trashed_property, False)
        query = obj.session.query(cls)
        if trashed == False:
            query = query.filter(cls._trashed == False)
        # run the query
        return query.filter(*criterion).limit(limit).offset(offset).all()
    
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
    
    def _commit(self):
        # success or rollback
        if self.success:
            self.session.commit()
        else:
            self.session.rollback()
            
    def save(self):
        if self._real_id is None:
            # generate id if not exists
            if self.id is None:
                self.generate_id()
            # insert
            self.before_insert()
            if self.success:
                self.session.add(self)
        else:
            self.before_update()
        self.before_save()
        self._commit()
    
    def trash(self):
        self.before_trash()
        if self.success:
            self._trashed = True
        self._commit()
    
    def untrash(self):
        self.before_untrash()
        if self.success:
            self._trashed = False
        self._commit()
    
    def delete(self):
        self.before_delete()
        if self.success:
            self.session.delete(self)
        self._commit()
    
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
    
    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
    
    def to_json(self):
        dictionary = self.to_dict()
        for key in dictionary:
            val = dictionary[key]
            if hasattr(val, 'to_dict'):
                val = val.to_dict()
            elif hasattr(val, 'isoformat'):
                val = val.isoformat()
            dictionary[key] = val
        return json.dumps(dictionary)