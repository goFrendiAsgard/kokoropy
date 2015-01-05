import re, getpass
from kokoropy import request
from kokoropy.model import DB_Model, or_, and_, Column, ForeignKey, func,\
    Integer, String, Date, DateTime, Boolean, Text, relationship, backref, association_proxy
from _config import session, encrypt_password
from _all import engine, Cms, Group, Third_Party_Authenticator, Page, Page_Groups,\
    Theme, Layout, Widget, Widget_Groups, User, User_Third_Party_Identities, User_Groups,\
    Language, Language_Detail, Configuration

def do_login(identity, password):
    user_list = User.get(and_(or_(User.username == identity, User.email == identity), User.encrypted_password == encrypt_password(password)))
    if len(user_list) > 0:
        user = user_list[0]
        request.SESSION['__user_id'] = user.id
        return True
    else:
        return False

def do_logout():
    request.SESSION.pop('__user_id', None)

def get_current_user():
    if '__user_id' in request.SESSION:
        user_id = request.SESSION['__user_id']
        user = User.find(user_id)
        return user
    return None

def get_pages(*criterion):
    current_user = get_current_user()
    is_super_admin = current_user.super_admin if current_user is not None else False
    current_user_id = current_user.id if current_user is not None else None

    try:
        subquery = session.query(func.count(Group.id).label('group_count'), Page_Groups.fk_page).\
                    join(User_Groups).\
                    join(User).\
                    join(Page_Groups).\
                    filter(User.id == current_user_id).\
                    subquery("subquery")

        return session.query(Page).\
            filter(Page.active == True).\
            filter(*criterion).\
            filter(
                    or_(
                            Page.authorization == 'everyone',                                       # EVERYONE
                            and_(Page.authorization == 'unauthenticated', current_user is None),    # UNAUTHENTICATED
                            and_(Page.authorization == 'authenticated', current_user is not None),  # AUTHENTICATED
                            and_(Page.authorization == 'authorized', is_super_admin),               # AUTHORIZED & Super Admin
                            and_(                                                                   # AUTHORIZED or STRICT_AUTHORIZED
                                    or_(
                                            Page.authorization == 'authorized', 
                                            Page.authorization == 'strict_authorized'
                                        ),
                                    and_( 
                                            subquery.c.group_count > 0,
                                            subquery.c.fk_page == Page._real_id
                                        )
                                )
                            
                        )
                ).\
            all()
    except Exception, e:
        session.rollback()
        raise

def get_widgets(*criterion):
    current_user = get_current_user()
    is_super_admin = current_user.super_admin if current_user is not None else False
    current_user_id = current_user.id if current_user is not None else None

    try:
        subquery = session.query(func.count(Group.id).label('group_count'), Widget_Groups.fk_widget).\
                    join(User_Groups).\
                    join(User).\
                    join(Widget_Groups).\
                    filter(User.id == current_user_id).\
                    subquery("subquery")

        return session.query(Widget).\
            filter(Widget.active == True).\
            filter(*criterion).\
            filter(
                    or_(
                            Widget.authorization == 'everyone',                                       # EVERYONE
                            and_(Widget.authorization == 'unauthenticated', current_user is None),    # UNAUTHENTICATED
                            and_(Widget.authorization == 'authenticated', current_user is not None),  # AUTHENTICATED
                            and_(Widget.authorization == 'authorized', is_super_admin),               # AUTHORIZED & Super Admin
                            and_(                                                                     # AUTHORIZED or STRICT_AUTHORIZED
                                    or_(
                                            Widget.authorization == 'authorized', 
                                            Widget.authorization == 'strict_authorized'
                                        ),
                                    and_( 
                                            subquery.c.group_count > 0,
                                            subquery.c.fk_widget == Widget._real_id
                                        )
                                )
                            
                        )
                ).\
            all()
    except Exception, e:
        session.rollback()
        raise

def insert_default():
    # default action
    if Group.count() == 0:
        super_admin = Group()
        super_admin.name = 'Super Admin'
        super_admin.save()
    else:
        super_admin = Group.get()[0]
    
    if User.count() == 0:
        print('No user registered to this system. Please add a new one !!!')
        username = raw_input('New user name : ')
        realname = raw_input('Real name : ')
        email = ''
        password = ''
        confirm_password = ''
        while True:
            email = raw_input('Email : ')
            if re.match(r'[^@]+@[^@]+\.[^@]+', email):
                break
            else:
                print('Invalid email address, please insert again')
        while True:
            password = getpass.getpass('Password : ')
            confirm_password = getpass.getpass('Password (again) :')
            if password == confirm_password:
                break
            else:
                print('Password doesn\'t match, please insert again')
        super_user = User()
        super_user.username = username
        super_user.realname = realname
        super_user.email = email
        super_user.password = password
        super_user.groups.append(super_admin)
        super_user.save()