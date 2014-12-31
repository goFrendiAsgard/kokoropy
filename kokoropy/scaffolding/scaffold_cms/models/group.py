from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option,\
    relationship, backref, association_proxy, creator_maker, fk_column,\
    one_to_many, many_to_one, lookup_proxy
from _config import session, metadata

DB_Model.metadata = metadata

class Group(DB_Model):
    __session__          = session
    __id_prefix__        = 'Group-'
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "user_groups"   : ["id", "group"],
            "page_groups"   : ["id", "group"],
            "widget_groups" : ["id", "group"]
        }
    __detail_excluded_form_column__ = {
            "user_groups"   : ["id", "group"],
            "page_groups"   : ["id", "group"],
            "widget_groups" : ["id", "group"]
        }
    # Column's Labels
    __column_label__ = {
            "user_groups"   : "Users",
            "page_groups"   : "Pages",
            "widget_groups" : "Widgets"
        }
    # Fields Declarations
    name                 = Column(String(50))
    active               = Column(Boolean)
    user_groups          = one_to_many("User_Groups", "User_Groups.fk_group")
    users                = lookup_proxy("user_groups", "User_Groups.user")
    page_groups          = one_to_many("Page_Groups", "Page_Groups.fk_group")
    pages                = lookup_proxy("page_groups", "Page_Groups.page")
    widget_groups        = many_to_one("Widget_Groups", "Widget_Groups.fk_group")
    widgets              = lookup_proxy("widget_groups", "Widget_Groups.widget")
    

