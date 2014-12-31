from kokoropy.model import DB_Model, auto_migrate
from _config import engine

from cms import Cms
from group import Group
from third_party_authenticator import Third_Party_Authenticator
from page import Page, Page_Groups
from theme import Theme
from layout import Layout
from widget import Widget, Widget_Groups
from user import User, User_Third_Party_Identities, User_Groups
from language import Language, Language_Detail
from configuration import Configuration


'''
 By using auto_migrate, kokoropy will automatically adjust your database schema
 based on DB_Model changes. However this is not always works. This method is merely
 there for the sake of easyness and not recommended for production environment.
'''
auto_migrate(engine)