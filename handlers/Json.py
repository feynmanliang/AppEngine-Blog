import json

from handlers.Blog import BlogHandler
from handlers.Blog import blog_key

from google.appengine.ext import db

## JSON
class JsonFeed(BlogHandler): 
    """ Generates a JSON object of articles (blog posts) """

    def get(self):
        articles = db.GqlQuery('SELECT * FROM Post '
                               'ORDER BY created DESC '
                               'LIMIT 20')
        articles = list(articles)
        content = [{'subject': article.subject,
                    'content': article.content,
                    'created': str(article.created.strftime('%a %b %d %H:%M:%S %Y')),
                    'last_modified': str(article.last_modified.strftime('%a %b %d %H:%M:%S %Y'))
                   } for article in articles]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(content, indent=4))

class JsonPost(BlogHandler): 
    """ Generates single JSON object of article """

    def get(self, resource):
        key = db.Key.from_path('Post', int(resource), parent=blog_key())
        article = db.get(key)

        content = [{'subject': article.subject,
                    'content': article.content,
                    'created': str(article.created.strftime('%a %b %d %H:%M:%S %Y')),
                    'last_modified': str(article.last_modified.strftime('%a %b %d %H:%M:%S %Y'))
                   }]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(content, indent=4))