from kokoropy.model import DB_Model, Ordered_DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option, RichText,\
    relationship, backref, association_proxy, creator_maker, fk_column,\
    one_to_many, many_to_one, lookup_proxy
from _config import session, metadata

DB_Model.metadata = metadata

class Village(DB_Model):
    __session__          = session
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "village_friends" : ["left_village"],
            "village_commodities" : ["village"]
        }
    __detail_excluded_form_column__ = {
            "village_friends" : ["left_village"],
            "village_commodities" : ["village"]
        }
    # Column's Labels
    __column_label__ = {
            "village_friends" : "Friends",
            "village_commodities" : "Commodities"
        }
    # Detail Column's Labels
    __detail_column_label__ = {
            "village_friends" : {
                "right_village" : "Name"
            }
        }
    # Fields Declarations
    name                 = Column(String(50))
    fk_clan              = fk_column("clan._real_id")
    clan                 = many_to_one("Clan", "Village.fk_clan")
    created              = Column(DateTime)
    level                = Column(Integer)
    active               = Column(Boolean)
    photo                = Column(Upload(is_image=True))
    village_friends      = one_to_many("Village_Friends", "Village_Friends.fk_left_village")
    friends              = lookup_proxy("village_friends", "Village_Friends.right_village")
    village_commodities  = one_to_many("Village_Commodities", "Village_Commodities.fk_village")
    commodities          = lookup_proxy("village_commodities", "Village_Commodities.resource")
    villagers            = one_to_many("Villager", "Villager.fk_village")
    important_structure  = one_to_many("Structure", "Structure.fk_village")
    description          = Column(RichText)

class Village_Friends(DB_Model):
    __session__          = session
    # Fields Declarations
    fk_left_village      = fk_column("village._real_id")
    fk_right_village     = fk_column("village._real_id")
    left_village         = many_to_one("Village", "Village_Friends.fk_left_village")
    right_village        = many_to_one("Village", "Village_Friends.fk_right_village")

class Village_Commodities(Ordered_DB_Model):
    __session__          = session
    # Fields Declarations
    fk_village           = fk_column("village._real_id")
    fk_resource          = fk_column("resource._real_id")
    village              = many_to_one("Village", "Village_Commodities.fk_village")
    resource             = many_to_one("Resource", "Village_Commodities.fk_resource")

