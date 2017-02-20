import time
import webapp2

from util import render_str, make_secure_val, check_secure_val, blog_key
from util import valid_username, valid_email, valid_password, get_post

from models.user import User
from models.post import Post
from models.comment import Comment

from decorator import login_required, post_exists, user_is_author
from decorator import user_is_not_author, user_is_comment_author


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


class MainPage(BlogHandler):
    def get(self):
        self.write('Hello, Udacity!')


class BlogFront(BlogHandler):
    def get(self):
        posts = Post.all().order('-created')
        if self.user:
            self.render('front-private.html', posts=posts,
                        user_name=self.user.name)
        else:
            self.render('front.html', posts=posts)


class PostPage(BlogHandler):
    @post_exists
    def get(self, post_id):
        post = get_post(post_id)
        self.render("permalink.html", post=post, user=self.user)


class NewPost(BlogHandler):
    @login_required
    def get(self):
        self.render("newpost.html")

    @login_required
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content,
                     author=self.user, likes=[])
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content,
                        error=error)


# Unit 2 HW's
class Rot13(BlogHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text=rot13)


class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Unit2Signup(Signup):
    def done(self):
        self.redirect('/unit2/welcome?username=' + self.username)


class Register(Signup):
    def done(self):
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'The username %s already exists.' % u.name
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/unit3/welcome')


class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/unit3/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg, username=username)


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')


class Unit3Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')


class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/unit2/signup')


class Like(BlogHandler):
    @post_exists
    @login_required
    @user_is_not_author
    def get(self, post_id):
        post = get_post(post_id)
        if self.user.name not in post.likes:
            post.likes.append(self.user.name)
            post.put()
            time.sleep(0.1)
        else:
            post.likes.remove(self.user.name)
            post.put()
            time.sleep(0.1)
        self.redirect('/blog/?')


class Edit(BlogHandler):
    @post_exists
    @user_is_author
    @login_required
    def get(self, post_id):
        post = get_post(post_id)
        self.render('edit.html', post=post)

    @post_exists
    @user_is_author
    @login_required
    def post(self, post_id):
        post = get_post(post_id)
        post.subject = self.request.get('subject')
        post.content = self.request.get('content')
        post.put()
        time.sleep(0.1)
        self.redirect('/blog')


class Delete(BlogHandler):
    @post_exists
    @user_is_author
    @login_required
    def get(self, post_id):
        post = get_post(post_id)
        self.render('delete.html', post=post)

    @post_exists
    @user_is_author
    @login_required
    def post(self, post_id):
        post = get_post(post_id)
        post.delete()
        time.sleep(0.1)
        self.redirect('/blog')


class NewComment(BlogHandler):
    @post_exists
    @login_required
    def get(self, post_id):
        post = get_post(post_id)
        self.render("new-comment.html", post=post)

    @post_exists
    @login_required
    def post(self, post_id):
        content = self.request.get('content')
        post = get_post(post_id)
        if content:
            c = Comment(content=content, author=self.user, likes=[],
                        post=post)
            c.put()
            time.sleep(0.1)
            self.redirect('/blog')
        else:
            error = "Please input Content!"
            self.render("new-comment.html", content=content, error=error)


class EditComment(BlogHandler):
    @user_is_comment_author
    @login_required
    def get(self, comment_id):
        comment = Comment.by_id(int(comment_id))
        self.render('comment-edit.html', comment=comment)

    @user_is_comment_author
    @login_required
    def post(self, comment_id):
        comment = Comment.by_id(int(comment_id))
        comment.content = self.request.get('content')
        comment.put()
        time.sleep(0.1)
        self.redirect('/blog')


class DeleteComment(BlogHandler):
    @user_is_comment_author
    @login_required
    def get(self, comment_id):
        comment = Comment.by_id(int(comment_id))
        self.render('comment-delete.html', comment=comment)

    @user_is_comment_author
    @login_required
    def post(self, comment_id):
        comment = Comment.by_id(int(comment_id))
        comment.delete()
        time.sleep(0.1)
        self.redirect('/blog')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/unit2/rot13', Rot13),
                               ('/unit2/signup', Unit2Signup),
                               ('/unit2/welcome', Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/unit3/welcome', Unit3Welcome),
                               ('/blog/([0-9]+)/like', Like),
                               ('/blog/([0-9]+)/edit', Edit),
                               ('/blog/([0-9]+)/delete', Delete),
                               ('/blog/([0-9]+)/comment', NewComment),
                               ('/blog/([0-9]+)/comment_edit', EditComment),
                               ('/blog/([0-9]+)/comment_delete', DeleteComment)
                               ],
                              debug=True)
