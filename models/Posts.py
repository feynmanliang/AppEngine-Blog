from google.appengine.ext import db

import jinja2
from handlers.base import jinja_env

class Post(db.Model):
    """Data model for individual blog post"""
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return self.render_str("post.html", p = self)