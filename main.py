import os
import logging

import webapp2
import jinja2
from google.appengine.api import users

import tools
import ds


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
    """General helper functions"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def make_cookie(self, name, val):
        cookie_val = tools.make_secure_val(val)
        return self.response.headers.add_header(
                                    'Set-Cookie',
                                    '%s=%s; Path=/; HttpOnly' % (name, cookie_val)
                                    )

    def read_cookie(self):
        user_key = self.request.cookies.get('user_key')
        return user_key and tools.check_secure_val(user_key)


class Front(Handler):
    def get(self):
        self.render('front.html')


class StudentPortal(Handler):
    def get(self):
        admin = users.is_current_user_admin()
        user_key = self.read_cookie()
        if not user_key:
            user_key = self.request.get('key')
        if user_key or admin:
            notes = ds.get_notes(user_key)
            student = ds.get_student(user_key)
            first_name = student.name.split()[0]
            drive_link = student.drive_link
            edit_note = ""
            if admin:
                edit_note = "<a href='/editnote?q={{n.key}}'>edit</a>" # start here
            self.render('student.html', name=first_name, notes=notes, drive=drive_link, edit_note=edit_note)
        else:
            self.redirect('/login')


class Login(Handler):
    def get(self):
        user_key = self.read_cookie()
        if user_key:
            self.redirect('/student')
        else:
            self.render('login.html')

    def post(self):
        user_name = self.request.get('username')
        user_pw = self.request.get('password')
        user_entry = ds.Students.by_user(user_name).get()
        if user_entry:
            user_key = user_entry.key.urlsafe()
            hashed = user_entry.password
            if tools.bcrypt.hashpw(user_pw, hashed) == hashed:
                self.make_cookie('user_key', user_key)
                self.redirect('/student')
        self.render('login.html', login_error='Invalid Login')


class Logout(Handler):
    def get(self):
        self.response.delete_cookie('user_key')
        self.redirect('/')


class AdminPortal(Handler):
    """===admin only access===

    This is the admin portal, can sign-up new students and add
    lesson notes here.
    """
    def get(self):
        students = ds.get_all_students()
        self.render('admin.html', students=students)


class AddNotes(Handler):
    """===admin only access===

    Validates and creates a new lesson notes entry
    """
    def get(self):
        user_key = self.request.get('key')
        student = ds.get_student(user_key)
        self.render('addnotes.html', student=student)

    def post(self):
        student = self.request.get('key')
        warmup = self.request.get('warmup')
        assign = self.request.get('assign')
        tips = self.request.get('tips')
        if student and warmup and assign and tips:
            notes = ds.write_notes(
                            student = student,
                            warmup = warmup,
                            tips = tips,
                            assign = assign
                            )
            self.redirect('/admin')
        else:
            error = "Please fill out all fields!"
            self.render('addnotes.html',
                        student = student,
                        warmup = warmup,
                        tips = tips,
                        assign = assign,
                        error = error)


class AddStudent(Handler):
    """===admin only access===

    Validates and creates a new student entity
    """
    def get(self):
        title = "New Student Signup"
        button_text = "Create"
        self.render('addstudent.html', title = title, button_text = button_text)

    def post(self):
        have_error = False
        name = self.request.get('name')
        user_name = self.request.get('username')
        user_pw = self.request.get('password')
        verify = self.request.get('verify')
        user_email = self.request.get('email')
        drive_link = self.request.get('drive')
        params = dict(username = user_name,
                      email = user_email)
        if not name:
            params['name_error']= "Please enter a name!"
            have_error = True
        if not tools.valid_username(user_name):
            params['username_error'] = "That's not a valid name!"
            have_error = True
        if ds.Students.by_user(user_name).get():
            params['name_error'] = "That user already exists!"
            have_error = True
        if not tools.valid_password(user_pw):
            params['password_error'] = "That's not a valid password!"
            have_error = True
        elif user_pw != verify:
            params['verify_error'] = "Passwords do not match!"
            have_error = True
        if not tools.valid_email(user_email):
            params['email_error'] = "That's not a valid email!"
            have_error = True
        if not drive_link:
            params['drive_error']= "Please enter Google Drive link!"
            have_error = True
        if have_error:
            self.render('addstudent.html', **params)
        else:
            hashed_pw = tools.password_protect(user_pw)
            user = ds.write_user(
                            user = user_name,
                            password = hashed_pw,
                            email = user_email,
                            name = name,
                            drive_link = drive_link
                            )
            self.redirect('/admin')


class EditStudent(Handler):
    """===admin only access===

    Edit a student entity
    """
    def get(self):
        if users.is_current_user_admin():
            title = "Edit Student Info"
            button_text = "Update"
            user_key = self.request.get('key')
            student = ds.get_student(user_key)
            self.render(
                    'addstudent.html',
                    title = title,
                    button_text = button_text,
                    name = student.name,
                    username = student.user,
                    password = 'noupdate',
                    email = student.email,
                    drive = student.drive_link
                    )
        else:
            self.redirect('/')

    def post(self):
        have_error = False
        pw = None
        pe = ""
        ve = ""
        user_key = self.request.get('key')
        name = self.request.get('name')
        user_name = self.request.get('username')
        user_pw = self.request.get('password')
        verify = self.request.get('verify')
        user_email = self.request.get('email')
        drive_link = self.request.get('drive')

        if user_pw != 'noupdate' or verify != 'noupdate':
            if not tools.valid_password(user_pw):
                have_error = True
                pe = "Thats not a valid password!"
            elif user_pw != verify:
                have_error = True
                ve = "Passwords do not match!"
            else:
                hashed_pw = tools.password_protect(user_pw)
                pw = hashed_pw

        if have_error:
            self.render(
                    'addstudent.html',
                    name = name,
                    username = user_name,
                    password = 'noupdate',
                    email = user_email,
                    drive = drive_link,
                    password_error = pe,
                    verify_error = ve
                    )
        else:
            ds.edit_user(
                    user_key,
                    pw,
                    user = user_name,
                    email = user_email,
                    name = name,
                    drive_link = drive_link
                    )
            self.redirect('/admin')


app = webapp2.WSGIApplication([
                        ('/', Front),
                        ('/addnotes', AddNotes),
                        ('/addstudent', AddStudent),
                        ('/login', Login),
                        ('/logout', Logout),
                        ('/student', StudentPortal),
                        ('/admin', AdminPortal),
                        ('/editstudent', EditStudent)
                        ], debug=True)
