from sqlalchemy import create_engine, Column, func, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime, time
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
    __idprefix__ = '%Y%m%d-'
    __digitprefix__ = 3
    
    def _init_db(self):
        # don't make session if it is already created
        if not hasattr(self, 'session'):
            self.engine = create_engine(self.__connectionstring__, echo=self.__echo__)
            self.session = scoped_session(sessionmaker(bind=self.engine))
            Base.metadata.create_all(bind=self.engine)
    
    def get(self, **kwargs):
        self._init_db()
        # get the class object and class name
        classobj = self.__class__
        classobj_name = classobj.__name__
        trashed_property = classobj_name + '._trashed'
        # define default value for limit and offset
        limit = kwargs.pop('_limit', 1000)
        offset = kwargs.pop('_offset', 0)
        # make query, by default trashed = False
        trashed = kwargs.pop(trashed_property, False)
        query = self.session.query(classobj)
        if trashed == False:
            query = query.filter(classobj._trashed == False)
        # run the query
        return query.filter(**kwargs).limit(limit).offset(offset).all()
    
    def save(self):
        self._init_db()
        if self._real_id is None:
            self.session.add(self)
            # generate id if not exists
            if self.id is None:
                self.generate_id()
            self.session.commit()
        self.session.commit()
        
    
    def trash(self):
        self._init_db()
        self._trashed = True
        self.session.commit()
    
    def untrash(self):
        self._init_db()
        self._trashed = False
        self.session.commit()
    
    def delete(self):
        self._init_db()
        self.session.delete(self)
        self.session.commit()
    
    def generate_id(self):
        if self.id is None:
            prefix = datetime.datetime.fromtimestamp(time.time()).strftime(self.__idprefix__)
            classobj = self.__class__
            # get maxid
            self._init_db()
            query = self.session.query(func.max(classobj.id).label("maxid")).filter(classobj.id.like(prefix+'%')).one()
            maxid = query.maxid
            if maxid is None:
                number = 0
            else:
                # get number part of maxid
                number = int(maxid[len(prefix):])
            # create newid
            newid = prefix + str(number+1).zfill(self.__digitprefix__)
            self.id = newid
    
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

if __name__ == '__main__':
    class Coba(Base, Mixin):
        __tablename__ = 'coba'
        __connectionstring__ = 'sqlite:///coba.db'
        __echo__ = False
        name = Column(String)
    coba = Coba()
    coba.name = 'Superman'
    coba.name = 'Clark Kent'
    coba.save()
    coba.trash()
    for obj in Coba().get():
        print(obj.to_dict())