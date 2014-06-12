import logging
import time

from google.appengine.api import memcache
from google.appengine.ext import ndb

from Notes import Notes
from Students import Students


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

def get_students():
    return Students.query().order(Students.user)

def write_notes(**kwargs):
    entry = Notes(**kwargs)
    entry.put()
    memcache.set(str(entry.key.id()), entry)
    entries_cache(update=True)
    return entry

def write_user(**kwargs):
    entry = Students(**kwargs)
    return entry.put()
