from google.appengine.ext import ndb


class Students(ndb.Model):
    user = ndb.StringProperty(required=True)
    password  = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty()

    @classmethod
    def by_user(cls, name):
        return cls.query(cls.user == name)

    @classmethod
    def by_id(cls, user_id):
        return cls.query(cls.key.id(user_id))