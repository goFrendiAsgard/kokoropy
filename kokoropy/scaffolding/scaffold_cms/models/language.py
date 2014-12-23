from sqlalchemy import or_, and_, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model
from _config import session, metadata

DB_Model.metadata = metadata

class Language(DB_Model):
    __session__ = session
    __id_prefix__        = 'Lang-'
    # Fields Declarations
    name                 = Column(String(50))
    iso_639_2            = Column(String(4))
    description          = Column(Text)
    detail               = relationship("Language_Detail", foreign_keys="Language_Detail.fk_language")

    def build_input_description(self, **kwargs):
        input_attribute = kwargs.pop('input_attribute', {})
        if 'name' not in input_attribute:
            input_attribute['name'] = 'description'
        value = self.description if self.description is not None else ''
        return '<textarea id="field_description" name="' + input_attribute['name'] + '" class="form-control" placeholder="Language Description">'+value+'</textarea>'


class Language_Detail(DB_Model):
    __session__ = session
    __id_prefix__        = 'LDet-'
    # Fields Declarations
    fk_language          = Column(Integer, ForeignKey("language._real_id"))
    word                 = Column(String(255))
    translation          = Column(String(255))
