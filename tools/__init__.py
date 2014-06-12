import re
import string
import hmac
import logging

import bcrypt

import config


### USERS ###
ADMIN_ID = config.data['admin']
def is_admin(user_id):
    """Checks user id for admin status"""
    return user_id == ADMIN_ID

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    """Validates user name"""
    return username and USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    """Validates user password"""
    return password and PW_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    """Validates user email"""
    return not email or EMAIL_RE.match(email)

def password_protect(pw):
    """Salts a user password for db entry"""
    return bcrypt.hashpw(pw, bcrypt.gensalt())


### COOKIES ###
SECRET = config.data['secret'] # config file is gitignored
def hash_str(s):
    """Creates new cookie hash"""
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    """Makes user id cookie"""
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    """Validates user id cookie"""
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val
