from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option, Code,\
    relationship, backref, association_proxy, creator_maker, fk_column,\
    one_to_many, many_to_one, lookup_proxy
from _config import session, metadata, authorization_options

DB_Model.metadata = metadata

class Page(DB_Model):
    __session__          = session
    __id_prefix__        = 'Page-'
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "page_groups" : ["id", "page"]
        }
    __detail_excluded_form_column__ = {
            "page_groups" : ["id", "page"]
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
    authorization        = Column(Option(50, options = authorization_options))
    page_order           = Column(Integer)
    page_groups          = one_to_many("Page_Groups.fk_page")
    groups               = lookup_proxy("page_groups", "Page_Groups.group")
    fk_page              = fk_column('page._real_id')
    parent               = many_to_one("Page", "Page.fk_page")
    fk_theme             = fk_column("theme._real_id")
    theme                = many_to_one("Theme", "Page.fk_theme")
    fk_layout            = fk_column("layout._real_id")
    layout               = many_to_one("Layout", "Page.fk_layout")
    active               = Column(Boolean)

    def before_save(self):
        if self.page_order is None:
            query = self.session.query(func.max(Page.page_order).label("max_page_order")).filter(Page.fk_parent_id == self.fk_parent_id).one()
            max_page_order = query.max_page_order
            if max_page_order is None:
                max_page_order = 0
            self.page_order = max_page_order

class Page_Groups(DB_Model):
    __session__          = session
    __id_prefix__        = 'PGroup-'
    # Fields Declarations
    fk_page              = fk_column("page._real_id")
    fk_group             = fk_column("group._real_id")
    page                 = relationship("Page", foreign_keys="Page_Groups.fk_page")
    group                = relationship("Group", foreign_keys="Page_Groups.fk_group")

