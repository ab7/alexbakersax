import os

import webapp2
import jinja2
from google.appengine.api import users

import tools
import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
    """General handler helper functions"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def make_cookie(self, name, val):
        cookie_val = tools.make_secure_val(str(val))
        return self.response.headers.add_header(
                                    'Set-Cookie',
                                    '%s=%s; Path=/' % (name, cookie_val)
                                    )

    def read_cookie(self):
        user_key = self.request.cookies.get('user_key')
        if user_key:
            return tools.check_secure_val(user_key)


class Front(Handler):
    def get(self):
        self.render('front.html')


class StudentPortal(Handler):
    def get(self):
        user_key = self.read_cookie()
        if not user_key:
            user_key = self.request.get('key')
        student = db.get_student(user_key)
        if user_key or users.is_current_user_admin():
            self.render('student.html', name=student.user)
        else:
            self.redirect('/')


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
        user_entry = db.Students.by_user(user_name).get()
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

    This is the admin portal, can signup new students and add
    lesson notes here.
    """
    def get(self):
        students = db.get_all_students()
        self.render('admin.html', students=students)


class NewStudent(Handler):
    """===admin only access===

    get - checks for admin and renders form
    post - validates and creates a new student entity
    """
    def get(self):
        self.render('newstudent.html')

    def post(self):
        have_error = False
        user_name = self.request.get('username')
        user_pw = self.request.get('password')
        verify = self.request.get('verify')
        user_email = self.request.get('email')
        params = dict(username = user_name,
                      email = user_email)
        if not tools.valid_username(user_name):
            params['name_error'] = "That's not a valid name!"
            have_error = True
        if db.Students.by_user(user_name).get():
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
        if have_error:
            self.render('newstudent.html', **params)
        else:
            hashed_pw = tools.password_protect(user_pw)
            user = db.write_user(
                            user = user_name,
                            password = hashed_pw,
                            email = user_email
                            )
            self.redirect('/admin')


class NewNotes(Handler):
    """===admin only access===

    get -- checks for admin and renders lesson notes form
    post -- validates and creates a new lesson notes entry
    """
    def render_newpost(self, subject="", content="", error=""):
        self.render('newnotes.html', subject=subject, content=content, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject and content:
            notes = db.write_notes(
                                subject = subject,
                                content = content
                                )
            self.redirect('/%d' % blog.key.id())
        else:
            error = "Please enter a subject AND content!"
            self.render_newpost(subject, content, error)


app = webapp2.WSGIApplication([
                        ('/', Front),
                        ('/newnotes', NewNotes),
                        ('/newstudent', NewStudent),
                        ('/login', Login),
                        ('/logout', Logout),
                        ('/student', StudentPortal),
                        ('/admin', AdminPortal)
                        ], debug=True)
