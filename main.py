import os
import re
import sys
import urllib2
import json



import webapp2
from webapp2 import WSGIApplication, Route
import jinja2

# set useful statics
root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'templates')
secret = 'In et arcu nulla, non accumsan nunc. Nullam vehicula dui.'

from handlers.Blog import *

from google.appengine.api import memcache
from google.appengine.ext import db

app = WSGIApplication([
    (r'/', 'handlers.Blog.MainPage'),
    (r'/rot13/?', 'handlers.Rot13.Rot13'),
    (r'/oldblog/?', 'handlers.OldBlog.MainPage'),
    (r'/oldblog/newpost', 'handlers.OldBlog.NewPost'),
    (r'/blog/?', 'handlers.Blog.BlogFront'),
    (r'/blog/([0-9]+)', 'handlers.Blog.PostPage'),
    (r'/blog/newpost/?', 'handlers.Blog.NewPost'),
    (r'/blog/signup/?', 'handlers.Auth.Signup'),
    (r'/blog/login', 'handlers.Auth.Login'),
    (r'/blog/logout', 'handlers.Auth.Logout'),
    (r'/blog/welcome/?', 'handlers.Auth.Welcome'),
    (r'/blog/.json', 'handlers.Json.JsonFeed'),
    (r'/blog/([0-9]+).json', 'handlers.Json.JsonPost'),
    (r'/blog/flush', 'handlers.Blog.CacheClear')
 ],
 debug=True)
