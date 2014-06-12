from google.appengine.ext import ndb


class Notes(ndb.Model):
    student_id = ndb.StringProperty(required = True)
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt)}
        return d