import hmac
import logging
import time

from handlers.base import AppHandler
from models.Posts import Post
from models.User import User
from main import secret

from google.appengine.ext import db
from google.appengine.api import memcache

def blog_key(name = 'default'):
        return db.Key.from_path('blogs', name)

class BlogHandler(AppHandler):
    """Handler for all links in blog application"""

    def make_secure_val(self, val):
        return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

    def check_secure_val(self, secure_val):
        val = secure_val.split('|')[0]
        if secure_val == self.make_secure_val(val):
            return val

    def set_secure_cookie(self, name, val):
        cookie_val = self.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and self.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        AppHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    def render_post(self, response, post):
        response.out.write('<b>' + post.subject + '</b><br>')
        response.out.write(post.content)

    def render_postlineitem(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)


class MainPage(BlogHandler):
  def get(self):
      self.write('Hello, Udacity! Go to: <a href="/blog">blog</a>')


##
## Memcached get contents
def getFront(update = False):
    cachekey = 'top'
    posts = memcache.get(cachekey)

    if posts is None or update:
        logging.error("DB QUERY")
        posts = db.GqlQuery("select * from Post order by created desc limit 10")

        posts = list(posts)
        memcache.set(cachekey, posts)
        memcache.set('update', time.time())
    return posts

def getPost(post_id, update = False):
    cachekey = 'permalink' + str(post_id)
    permalink = memcache.get(cachekey)

    if permalink is None or update:
        logging.error("DB QUERY")
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        permalink = db.get(key)

        memcache.set(cachekey, permalink)
        memcache.set('update_'+str(post_id), time.time())
    return permalink


##
## Content handlers
class BlogFront(BlogHandler):
    def get(self):
        posts = getFront()
        timesince = int(time.time() - memcache.get('update'))
        self.render('front.html', posts = posts, timesince = timesince)

class PostPage(BlogHandler):
    def get(self, post_id):
        # key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        # post = db.get(key)

        # if not post:
        #     self.error(404)
        #     return
        post = getPost(post_id)
        updateid = 'update_' + str(post_id)
        timesince = int(time.time() - memcache.get(updateid))

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post, timesince = timesince)

class NewPost(BlogHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            getFront(update=True)
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)
