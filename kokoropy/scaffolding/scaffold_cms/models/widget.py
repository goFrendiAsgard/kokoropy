from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option,\
    relationship, backref, association_proxy, creator_maker, fk_column,\
    one_to_many, many_to_one, lookup_proxy
from _config import session, metadata, authorization_options

DB_Model.metadata = metadata

class Widget(DB_Model):
    __session__          = session
    __id_prefix__        = 'Widget-'
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "widget_groups" : ["id", "widget"]
        }
    __detail_excluded_form_column__ = {
            "widget_groups" : ["id", "widget"]
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
    widget_groups        = one_to_many("Widget_Groups", "Widget_Groups.fk_widget")
    groups               = lookup_proxy("widget_groups", 'Widget_Groups.group')
    active               = Column(Boolean)

class Widget_Groups(DB_Model):
    __session__          = session
    __id_prefix__        = 'WGroup-'
    # Fields Declarations
    fk_widget            = fk_column("widget._real_id")
    fk_group             = fk_column("group._real_id")
    widget               = many_to_one("Widget", "Widget_Groups.fk_widget")
    group                = many_to_one("Group", "Widget_Groups.fk_group")

