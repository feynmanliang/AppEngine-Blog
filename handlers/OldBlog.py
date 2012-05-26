import os
import re
import sys
import urllib2
import random
import logging
from xml.dom import minidom
from string import letters

import webapp2
import jinja2
from main import template_dir

from google.appengine.api import memcache
from google.appengine.ext import db

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

class Entries(db.Model):
    title = db.StringProperty(required = True)
    entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self):
        self._render_text = self.entry.replace('\n', '<br>')
        return self.render_str("post.html", p = self)

class MainPage(Handler):
    def render_page(self):
        entries = db.GqlQuery("SELECT * FROM Entries "
                              "ORDER BY created DESC")
        self.render("front.html", posts=entries)

    def get(self):
        self.render_page()

class NewPost(Handler):
    def render_page(self, title="", entry="", error=""):
        self.render("form.html", title=title, entry=entry, error=error)

    def get(self):
        self.render_page()

    def post(self):
        title = self.request.get("title")
        entry = self.request.get("entry")

        if title and entry:
            a = Entries(title = title, entry = entry)
            a.put()

            self.redirect("/oldblog")
        else:
            error = "we need both a title and entry text!"
            self.render_front(title, entry, error)