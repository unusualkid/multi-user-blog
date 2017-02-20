from functools import wraps
from util import get_post
from models.comment import Comment


# Decorator for checking if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        if not self.user:
            self.redirect('/login')
        return f(self, *args, **kwargs)
    return decorated_function


# Decorator for checking if post exists, else throws 404
def post_exists(f):
    @wraps(f)
    def decorated_function(self, post_id, *args, **kwargs):
        post = get_post(post_id)
        if not post:
            self.error(404)
            return
        return f(self, post_id, *args, **kwargs)
    return decorated_function


# Decorator for checking if user is logged in
def user_is_author(f):
    @wraps(f)
    def decorated_function(self, post_id, *args, **kwargs):
        user_name = self.user.name
        post = get_post(post_id)
        if user_name == post.author.name:
            return f(self, post_id, *args, **kwargs)
        else:
            self.redirect('/blog')
    return decorated_function


# Decorator for checking is user is post author
def user_is_not_author(f):
    @wraps(f)
    def decorated_function(self, post_id, *args, **kwargs):
        user_name = self.user.name
        post = get_post(post_id)
        if user_name != post.author.name:
            return f(self, post_id, *args, **kwargs)
        else:
            self.redirect('/blog')
    return decorated_function


# Decorator for checking is user is comment author
def user_is_comment_author(f):
    @wraps(f)
    def decorated_function(self, comment_id, *args, **kwargs):
        user_name = self.user.name
        comment = Comment.by_id(int(comment_id))
        if user_name == comment.author.name:
            return f(self, comment_id, *args, **kwargs)
        else:
            self.redirect('/blog')
    return decorated_function
