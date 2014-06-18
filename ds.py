import logging
import time

from google.appengine.api import memcache
from google.appengine.ext import ndb



#####################################
###   ndb convenience functions   ###
#####################################

### read functions ###
def get_all_students():
    """Returns all Students entities"""
    students = memcache.get('students')
    update = memcache.get('student-update')
    if students and not update:
        # Should always return this unless a new student is added
        return students
    else:
        logging.error('NDB QUERY')
        students = Students.query()
        memcache.set('students', students)
        memcache.delete('update')
        students_by_name = students.order(Students.user)
        return students_by_name

def get_student(user_key):
    """Takes the encrypted student key and returns the student entity"""
    students = get_all_students()
    decoded_key = ndb.Key(urlsafe=user_key)
    student = students.filter(Students.key == decoded_key).get()
    return student

def get_notes(user_key):
    """Returns all lesson notes based on student key value"""
    notes = memcache.get(user_key)
    update = memcache.get(user_key + '-update')
    if notes and not update:
        # Should always return this unless notes have been added

        notes_by_date = notes.order(-Notes.created)
        return notes_by_date
    else:
        logging.error('NDB QUERY')
        notes = Notes.query(Notes.student == user_key)
        memcache.set(user_key, notes)
        memcache.delete(user_key + '-update')
        notes_by_date = notes.order(-Notes.created)
        return notes_by_date


### write functions ###
def write_notes(**kwargs):
    entry = Notes(**kwargs)
    entry.put()
    memcache.set('notes-update', True)
    return entry

def write_user(**kwargs):
    entry = Students(**kwargs)
    memcache.set('student-update', True)
    return entry.put()


######################
###   ndb models   ###
######################

class Notes(ndb.Model):
    """Lesson note entities"""
    student = ndb.StringProperty(required = True)
    warmup = ndb.TextProperty(required = True, indexed=False)
    assign = ndb.TextProperty(required = True, indexed=False)
    tips = ndb.TextProperty(required = True, indexed=False)
    created = ndb.DateTimeProperty(auto_now_add = True)


class Students(ndb.Model):
    """Student info entities"""
    user = ndb.StringProperty(required=True)
    password  = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True, indexed=False)
    drive_link = ndb.StringProperty(required = True, indexed=False)

    @classmethod
    def by_user(cls, name):
        return cls.query(cls.user == name)
