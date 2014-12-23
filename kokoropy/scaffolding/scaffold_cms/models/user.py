from sqlalchemy import or_, and_, Column, ForeignKey, func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from kokoropy.model import DB_Model
from _config import session, metadata

DB_Model.metadata = metadata

class User(DB_Model):
    __session__ = session
    # Excluded Columns
    __detail_excluded_shown_column__ = {
            "user_third_party_identities" : ["user"],
            "user_groups" : ["user"]
        }
    __detail_excluded_form_column__ = {
            "user_third_party_identities" : ["user"],
            "user_groups" : ["user"]
        }
    # Column's Labels
    __column_label__ = {
            "user_third_party_identities" : "Third Party Identities",
            "user_groups" : "Groups"
        }
    # Fields Declarations
    username             = Column(String(255))
    realname             = Column(String(255))
    email                = Column(String(255))
    photo                = Column(String(255))
    encrypted_password   = Column(String(255))
    user_groups          = relationship("User_Groups", foreign_keys="User_Groups.fk_user")
    groups               = association_proxy("user_groups", "fk_group", creator = lambda _val : User_Groups(group = _val))
    user_third_party_identities = relationship("User_Third_Party_Identities", foreign_keys="User_Third_Party_Identities.fk_user")
    third_party_identities = association_proxy("user_third_party_identities", "fk_third_party_authenticator", creator = lambda _val : User_Third_Party_Identities(third_party_authenticator = _val))
    last_login           = Column(DateTime)
    active               = Column(Boolean)
    fk_language          = Column(Integer, ForeignKey("language._real_id"))
    language             = relationship("Language", foreign_keys="User.fk_language")

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
    
    def build_custom_input(self, column_name, **kwargs):
        if column_name == 'password':
            return '<input id="field-password" name="password" placeholder="password">'
        else:
            return None

class User_Third_Party_Identities(DB_Model):
    __session__ = session
    # Fields Declarations
    fk_user              = Column(Integer, ForeignKey("user._real_id"))
    fk_third_party_authenticator = Column(Integer, ForeignKey("third_party_authenticator._real_id"))
    user                 = relationship("User", foreign_keys="User_Third_Party_Identities.fk_user")
    third_party_authenticator = relationship("Third_Party_Authenticator", foreign_keys="User_Third_Party_Identities.fk_third_party_authenticator")

class User_Groups(DB_Model):
    __session__ = session
    # Fields Declarations
    fk_user              = Column(Integer, ForeignKey("user._real_id"))
    fk_group             = Column(Integer, ForeignKey("group._real_id"))
    user                 = relationship("User", foreign_keys="User_Groups.fk_user")
    group                = relationship("Group", foreign_keys="User_Groups.fk_group")

