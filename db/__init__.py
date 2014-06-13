import logging
import time

from google.appengine.api import memcache
from google.appengine.ext import ndb

from Notes import Notes
from Students import Students

### memcache convenience functions ###
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


### database write convenience functions ###
def write_notes(**kwargs):
    entry = Notes(**kwargs)
    entry.put()
    memcache.set(str(entry.key.id()), entry)
    entries_cache(update=True)
    return entry

def write_user(**kwargs):
    entry = Students(**kwargs)
    return entry.put()
