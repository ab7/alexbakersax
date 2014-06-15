import logging
import time

from google.appengine.api import memcache
from google.appengine.ext import ndb



#####################################
###   ndb convenience functions   ###
#####################################

def entries_cache(key_='top', update=False):
    items = memcache.get(key_)
    if items is None or update:
        logging.error("NDB QUERY")
        if key_.isdigit():
            entry = Notes.get_by_id(int(key_))
            memcache.set(key_, entry)
            items = entry
        else:
            items = Notes.query().order(-Notes.created).fetch(10)
            memcache.set(key_, items)
        memcache.set('query_time', time.time())
    return items


### database retrieval convenience functions ###
def get_all_students():
    """Returns all Students entities"""
    return Students.query().order(Students.user)

def get_student(user_key):
    """Takes the encrypted student key and returns the student entity"""
    decoded_key = ndb.Key(urlsafe=user_key)
    return decoded_key.get()

def get_notes(user_key):
    """Returns all lesson notes based on student key value"""
    notes = Notes.query(Notes.student == user_key).order(-Notes.created)
    return notes


### database write convenience functions ###
def write_notes(**kwargs):
    entry = Notes(**kwargs)
    entry.put()
    return entry

def write_user(**kwargs):
    entry = Students(**kwargs)
    return entry.put()


######################
###   ndb models   ###
######################

class Notes(ndb.Model):
    """Lesson note entities"""
    student = ndb.StringProperty(required = True)
    warmup = ndb.TextProperty(required = True)
    assign = ndb.TextProperty(required = True)
    tips = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)


class Students(ndb.Model):
    """Student info entities"""
    user = ndb.StringProperty(required=True)
    password  = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty()
    name = ndb.StringProperty()

    @classmethod
    def by_user(cls, name):
        return cls.query(cls.user == name)
