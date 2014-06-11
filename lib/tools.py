import re
import string
import hmac

import bcrypt

import config


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
    
PW_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PW_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def password_protect(pw):
    return bcrypt.hashpw(pw, bcrypt.gensalt())

SECRET = config.stuff['secret']
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val              