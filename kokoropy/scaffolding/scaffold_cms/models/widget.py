from sqlalchemy import or_, and_, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model
from _config import session, metadata

DB_Model.metadata = metadata

class Widget(DB_Model):
    __session__ = session
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "widget_groups" : ["widget"]
        }
    __detail_excluded_form_column__ = {
            "widget_groups" : ["widget"]
        }
    # Column's Labels
    __column_label__ = {
            "widget_groups" : "Groups"
        }
    # Fields Declarations
    name                 = Column(String(50))
    static               = Column(Boolean)
    url                  = Column(String(255))
    static_content       = Column(Text)
    authorization        = Column(Integer)
    widget_groups        = relationship("Widget_Groups", foreign_keys="Widget_Groups.fk_widget")
    groups               = association_proxy("widget_groups", "fk_group", creator = lambda _val : Widget_Groups(group = _val))
    active               = Column(Boolean)

    def build_input_static_content(self, **kwargs):
        input_attribute = kwargs.pop('input_attribute', {})
        if 'name' not in input_attribute:
            input_attribute['name'] = 'content'
        value = self.static_content if self.static_content is not None else ''
        return '<textarea id="field_static_content" name="' + input_attribute['name'] + '" class="form-control" placeholder="Content">'+value+'</textarea>'


class Widget_Groups(DB_Model):
    __session__ = session
    # Fields Declarations
    fk_widget            = Column(Integer, ForeignKey("widget._real_id"))
    fk_group             = Column(Integer, ForeignKey("group._real_id"))
    widget               = relationship("Widget", foreign_keys="Widget_Groups.fk_widget")
    group                = relationship("Group", foreign_keys="Widget_Groups.fk_group")

