from sqlalchemy import or_, and_, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model
from _config import session, metadata

DB_Model.metadata = metadata

class Layout(DB_Model):
    __session__ = session
    __id_prefix__        = 'Layout-'
    # Fields Declarations
    fk_theme             = Column(Integer, ForeignKey("theme._real_id"))
    name                 = Column(String(50))
    content              = Column(Text)

    def build_input_content(self, **kwargs):
        input_attribute = kwargs.pop('input_attribute', {})
        if 'name' not in input_attribute:
            input_attribute['name'] = 'content'
        value = self.content if self.content is not None else ''
        return '<textarea id="field_content" name="' + input_attribute['name']  +'" class="form-control" placeholder="Content">'+value+'</textarea>'


