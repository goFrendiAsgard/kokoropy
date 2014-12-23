from sqlalchemy import or_, and_, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model
from _config import session, metadata

DB_Model.metadata = metadata

class Page(DB_Model):
    __session__ = session
    __id_prefix__        = 'Page-'
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "page_groups" : ["page"]
        }
    __detail_excluded_form_column__ = {
            "page_groups" : ["page"]
        }
    # Column's Labels
    __column_label__ = {
            "page_groups" : "Groups"
        }
    # Fields Declarations
    name                 = Column(String(50))
    title                = Column(String(255))
    meta_author          = Column(String(255))
    meta_keyword         = Column(Text)
    meta_description     = Column(Text)
    static               = Column(Boolean)
    url                  = Column(String(255))
    static_content       = Column(Text)
    authorization        = Column(Integer)
    page_order           = Column(Integer)
    page_groups          = relationship("Page_Groups", foreign_keys="Page_Groups.fk_page")
    groups               = association_proxy("page_groups", "fk_group", creator = lambda _val : Page_Groups(group = _val))
    fk_page              = Column(Integer, ForeignKey("page._real_id"))
    parent               = relationship("Page", foreign_keys="Page.fk_page")
    fk_theme             = Column(Integer, ForeignKey("theme._real_id"))
    theme                = relationship("Theme", foreign_keys="Page.fk_theme")
    fk_layout            = Column(Integer, ForeignKey("layout._real_id"))
    layout               = relationship("Layout", foreign_keys="Page.fk_layout")
    active               = Column(Boolean)

    def after_save(self):
        if self.page_order is None:
            query = self.session.query(func.max(Page.page_order).label("max_page_order")).filter(Page.fk_parent_id == self.fk_parent_id).one()
            max_page_order = query.max_page_order
            if max_page_order is None:
                max_page_order = 0
            self.page_order = max_page_order
    
    def build_input_static_content(self, **kwargs):
        input_attribute = kwargs.pop('input_attribute', {})
        if 'name' not in input_attribute:
            input_attribute['name'] = 'static_content'
        value = self.static_content if self.static_content is not None else ''
        return '<textarea id="field_static_content" name="' + input_attribute['name'] + '" class="form-control" placeholder="Content">'+value+'</textarea>'

    def build_input_meta_description(self, **kwargs):
        input_attribute = kwargs.pop('input_attribute', {})
        if 'name' not in input_attribute:
            input_attribute['name'] = 'meta_description'
        value = self.meta_description if self.meta_description is not None else ''
        return '<textarea id="field_meta_description" name="' + input_attribute['name'] + '" class="form-control" placeholder="Meta Description">'+value+'</textarea>'


class Page_Groups(DB_Model):
    __session__ = session
    # Fields Declarations
    fk_page              = Column(Integer, ForeignKey("page._real_id"))
    fk_group             = Column(Integer, ForeignKey("group._real_id"))
    page                 = relationship("Page", foreign_keys="Page_Groups.fk_page")
    group                = relationship("Group", foreign_keys="Page_Groups.fk_group")

