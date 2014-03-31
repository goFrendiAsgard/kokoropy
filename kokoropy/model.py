from sqlalchemy import create_engine, Column, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime, time, json
# create Base
Base = declarative_base()

class Mixin(object):
    _real_id = Column(Integer, primary_key=True)
    _trashed = Column(Boolean, default=False)
    _created_at = Column(DateTime, default=func.now())
    _updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    id = Column(String, unique=True)
    
    __connectionstring__ = ''
    __echo__ = True
    __prefixid__ = '%Y%m%d-'
    __digitid__ = 3
    
    @property
    def engine(self):
        if not hasattr(self, '_engine'):
            self._engine = create_engine(self.__connectionstring__, echo=self.__echo__)
        return self._engine
    
    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = scoped_session(sessionmaker(bind=self.engine))
        return self._session
    '''
    def _init_db(self):
        # don't make session if it is already created
        if not hasattr(self, 'session'):
            self.engine = create_engine(self.__connectionstring__, echo=self.__echo__)
            self.session = scoped_session(sessionmaker(bind=self.engine))
    '''
    
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
    
    def save(self):
        #self._init_db()
        if self._real_id is None:
            self.session.add(self)
            # generate id if not exists
            if self.id is None:
                self.generate_id()
        self.session.commit()
        
    
    def trash(self):
        #self._init_db()
        self._trashed = True
        self.session.commit()
    
    def untrash(self):
        #self._init_db()
        self._trashed = False
        self.session.commit()
    
    def delete(self):
        #self._init_db()
        self.session.delete(self)
        self.session.commit()
    
    def generate_prefix_id(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime(self.__prefixid__)
    
    def generate_id(self):
        if self.id is None:
            prefix = self.generate_prefix_id()
            classobj = self.__class__
            # get maxid
            #self._init_db()
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