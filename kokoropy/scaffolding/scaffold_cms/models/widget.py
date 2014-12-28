from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Option, relationship, backref, association_proxy
from _config import session, metadata, authorization_options

DB_Model.metadata = metadata

class Widget(DB_Model):
    __session__          = session
    __id_prefix__        = 'Widget-'
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
    authorization        = Column(Option(50, options = authorization_options))
    widget_groups        = relationship("Widget_Groups", foreign_keys="Widget_Groups.fk_widget")
    groups               = association_proxy("widget_groups", "fk_group", creator = lambda _val : Widget_Groups(group = _val))
    active               = Column(Boolean)

class Widget_Groups(DB_Model):
    __session__          = session
    __id_prefix__        = 'WGroup-'
    # Fields Declarations
    fk_widget            = Column(Integer, ForeignKey("widget._real_id"))
    fk_group             = Column(Integer, ForeignKey("group._real_id"))
    widget               = relationship("Widget", foreign_keys="Widget_Groups.fk_widget")
    group                = relationship("Group", foreign_keys="Widget_Groups.fk_group")

