import re, getpass
from kokoropy import request
from structure import *

def do_login(identity, password):
    user_list = User.get(and_(or_(User.username == identity, User.email == identity), User.encrypted_password == encrypt_password(password)))
    if len(user_list) > 0:
        user = user_list[0]
        request.SESSION['__user_id'] = user.id
        return True
    else:
        return False

def do_logout():
    if '__user_id' in request.SESSION:
        request.SESSION.remove('__user_id')

def get_current_user():
    if '__user_id' in request.SESSION:
        user_id = request.SESSION['__user_id']
        user = User.find(user_id)
        return user

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
