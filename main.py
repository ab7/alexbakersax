import os
import json

import webapp2
import jinja2

from lib import tools
from data import dbc

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

    def make_cookie(self, name, val):
        cookie_val = tools.make_secure_val(str(val))
        return self.response.headers.add_header(
                        'Set-Cookie', 
                        '%s=%s; Path=/' % (name, cookie_val)
                        )
      
    def read_cookie(self, user_id):
        if user_id:
            if tools.check_secure_val(user_id): 
                return True
        
class Front(Handler):
    def get(self):
        user_cookie = self.request.cookies.get('user_id')
        if self.read_cookie(user_cookie):
            self.render("welcome.html")
        else:
            self.render("front.html")

class Permalink(Handler):
    def get(self, blog_id):
        b = dbc.entries_cache(blog_id)
        seconds = dbc.query_time()
        if self.request.url.endswith('.json'):
            self.render_json(b.as_dict())
        else:
            self.render("front.html", blogs=[b], seconds=seconds)

class NewPost(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)
    
    def get(self):
        self.render_newpost()
        
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            notes = dbc.write_notes(subject = subject,
                                  subject_uri = subject_uri,
                                  content = content)
            self.redirect("/%d" % blog.key.id())
        else:
            error = "Please enter a subject AND content!"
            self.render_newpost(subject, content, error)

class Signup(Handler):   
    def get(self):
        self.render('signup.html')
        
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

        if dbc.Students.by_user(user_name).get():
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
            self.render('signup.html', **params)
        else:
            hashed_pw = tools.password_protect(user_pw)
            user = dbc.write_user(user = user_name, 
                                  password = hashed_pw, 
                                  email = user_email
                                )
            self.make_cookie('user_id', user.id())
            self.redirect('/welcome')

class Login(Handler):
    def get(self):    
        self.render('login.html')

    def post(self):
        user_name = self.request.get('username')
        user_pw = self.request.get('password')
        user_entry = dbc.Students.by_user(user_name).get()

        if user_entry:
            user_id = user_entry.key.id()
            hashed = user_entry.password

            if tools.bcrypt.hashpw(user_pw, hashed) == hashed:
                self.make_cookie('user_id', user_id)
                self.redirect('/welcome')

        self.render('login.html', login_error="Invalid Login")

class Logout(Handler):
    def get(self):
        self.response.delete_cookie('user_id')
        self.redirect('/')

class Welcome(Handler):
    def get(self):
        id_cookie_str = self.request.cookies.get('user_id')
        user_id = None
        if id_cookie_str:
            val = tools.check_secure_val(id_cookie_str)
            if val:
                id_convert = int(id_cookie_str.split('|')[0])
                user = dbc.Students.get_by_id(id_convert).user
            else:
                self.redirect('/')          
        else:
            self.redirect('/')

        self.render('welcome.html', name=user)

        
app = webapp2.WSGIApplication([('/', Front),
                               ('/([0-9]+)?(?:.json)?', Permalink),
                               ('/newpost', NewPost), 
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', Welcome)
                            ], debug=True)