from sqlalchemy import or_, and_, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model
from _config import session, metadata

DB_Model.metadata = metadata

class Configuration(DB_Model):
    __session__ = session
    __id_prefix__        = 'Conf-'
    # Fields Declarations
    name                 = Column(String(50))
    value                = Column(Text)

    def build_input_description(self, **kwargs):
        input_attribute = kwargs.pop('input_attribute', {})
        if 'name' not in input_attribute:
            input_attribute['name'] = 'description'
        value = self.value if self.value is not None else ''
        return '<textarea id="field_value" name="' + input_attribute['name'] + '" class="form-control" placeholder="Configuration Value">'+value+'</textarea>'


