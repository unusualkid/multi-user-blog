from util import render_str
from google.appengine.ext import db
from user import User


class Post(db.Model):
    subject = db.StringProperty()
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.ReferenceProperty(User, collection_name="posts")
    # a list of user.name that liked the post
    likes = db.StringListProperty()

    def render(self, **kwargs):
        if kwargs != {}:
            user = kwargs['user']
            if user:
                # to escape the characters \n
                self._render_text = self.content.replace('\n', '<br>')
                return render_str("post-private.html", post=self,
                                  user_name=user.name)
        else:
            self._render_text = self.content.replace('\n', '<br>')
            return render_str("post.html", post=self)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)
