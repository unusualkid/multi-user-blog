from google.appengine.ext import db
from post import Post
from user import User


class Comment(db.Model):
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.ReferenceProperty(User, collection_name="comments")
    post = db.ReferenceProperty(Post, collection_name="comments")

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)
