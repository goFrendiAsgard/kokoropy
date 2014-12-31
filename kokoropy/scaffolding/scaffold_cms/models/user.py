from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, Upload, Option,\
    relationship, backref, association_proxy, creator_maker, fk_column,\
    one_to_many, many_to_one, lookup_proxy
from _config import session, metadata, encrypt_password

DB_Model.metadata = metadata

class User(DB_Model):
    __session__                 = session
    __id_prefix__               = 'User-'
    __virtual_form_column__     = ['password']
    __excluded_form_column__    = ['encrypted_password']
    __excluded_shown_column__   = ['encrypted_password']
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "user_third_party_identities" : ["id", "user"],
            "user_groups" : ["id", "user"]
        }
    __detail_excluded_form_column__ = {
            "user_third_party_identities" : ["id", "user"],
            "user_groups" : ["id", "user"]
        }
    # Column's Labels
    __column_label__ = {
            "user_third_party_identities" : "Third Party Identities",
            "user_groups" : "Groups"
        }
    # Fields Declarations
    username                    = Column(String(255))
    realname                    = Column(String(255))
    email                       = Column(String(255))
    photo                       = Column(Upload(255, is_image=True))
    encrypted_password          = Column(String(255))
    super_admin                 = Column(Boolean)
    last_login                  = Column(DateTime)
    active                      = Column(Boolean)
    fk_language                 = fk_column("language._real_id")    
    user_groups                 = one_to_many("User_Groups", "User_Groups.fk_user")
    groups                      = lookup_proxy("user_groups", "User_Groups.group")
    user_third_party_identities = one_to_many("User_Third_Party_Identities", "User_Third_Party_Identities.fk_user")
    third_party_identities      = lookup_proxy("user_third_party_identities", "User_Third_Party_Idetities.third_party_authenticator")
    language                    = many_to_one("Language", "User.fk_language")

    @property
    def password(self):
        return None
    
    @password.setter
    def password(self, value):
        self.encrypted_password = encrypt_password(value)
    
    def assign_from_dict(self, variable):
        DB_Model.assign_from_dict(self, variable)
        if 'password' in variable and variable['password'] is not None and variable['password'] != '':
            self.password = variable['password']
    
    def build_input_password(self,  **kwargs):
        return '<input id="field-password" type="password" class="form-control" name="password" placeholder="password">'

class User_Third_Party_Identities(DB_Model):
    __session__                     = session
    __id_prefix__                   = 'UAuth-'
    # Fields Declarations
    fk_user                         = fk_column("user._real_id")
    fk_third_party_authenticator    = fk_column("third_party_authenticator._real_id")
    user                            = many_to_one("User", "User_Third_Party_Identities.fk_user")
    third_party_authenticator       = many_to_one("Third_Party_Authenticator", "User_Third_Party_Identities.fk_third_party_authenticator")

class User_Groups(DB_Model):
    __session__          = session
    __id_prefix__        = 'UGroup-'
    # Fields Declarations
    fk_user              = fk_column("user._real_id")
    fk_group             = fk_column("group._real_id")
    user                 = many_to_one("User", "User_Groups.fk_user")
    group                = many_to_one("Group","User_Groups.fk_group")