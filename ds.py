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
    if not students or update:
        logging.error('NDB QUERY')
        students = Students.query()
        memcache.set('students', students)
        memcache.delete('student-update')
    students_by_name = students.order(Students.user)
    return students_by_name

def get_student(user_key):
    """Takes the encrypted student key and returns the student entity"""
    students = get_all_students()
    decoded_key = ndb.Key(urlsafe=user_key)
    student = students.filter(Students.key == decoded_key).get()
    return student

def get_notes(user_key):
    """Returns all lesson notes based on student key"""
    notes = memcache.get(user_key)
    update = memcache.get(user_key + '-update')
    if not notes or update:
        logging.error('NDB QUERY')
        notes = Notes.query()
        memcache.set(user_key, notes)
        memcache.delete(user_key + '-update')
    student_notes = notes.filter(Notes.student == user_key)
    notes_by_date = student_notes.order(-Notes.created)
    return notes_by_date

def get_single_note(user_key, note_key):
    decoded_key = ndb.Key(urlsafe=note_key)
    all_notes = get_notes(user_key)
    note = all_notes.filter(Notes.key == decoded_key).get()
    return note

def get_latest_notes(user_key):
    all_notes = get_notes(user_key)
    return all_notes.fetch(1)[0]


### write functions ###
def write_notes(**kwargs):
    entry = Notes(**kwargs)
    memcache.set(entry.student + '-update', True)
    return entry.put()

def write_user(**kwargs):
    entry = Students(**kwargs)
    memcache.set('student-update', True)
    return entry.put()

def edit_user(user_key, pw, user, email, name, drive_link):
    student = get_student(user_key)
    student.user = user
    student.email = email
    student.name = name
    student.drive_link = drive_link
    if pw:
        student.password = pw
    memcache.set('student-update', True)
    return student.put()

def edit_note(note_key, student, warmup, assign, tips):
    note = get_single_note(student, note_key)
    note.warmup = warmup
    note.assign = assign
    note.tips = tips
    memcache.set(student + '-update', True)
    return note.put()



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
