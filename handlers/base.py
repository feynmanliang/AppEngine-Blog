import jinja2
import webapp2

from main import template_dir

# init jinja2 envi
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class AppHandler(webapp2.RequestHandler):
    """Base handler, encapsulating jinja2."""

    def __init__(self, request=None, response=None):
        """Initialize handler."""
        super(AppHandler, self).__init__(request, response)
        self.jinja2 = jinja_env

    def write(self, string):
        """Write arbitrary string to response stream."""
        self.response.out.write(string)

    def render_str(self, template_name, values=None, **kwargs):
        """Render jinja2 template and returns as string"""
        template = self.jinja2.get_template(template_name)
        return template.render(values or kwargs)

    def render(self, template_name, values=None, **kwargs):
        """Render jinja2 template using dictionary or kwargs"""
        self.write(self.render_str(template_name, values or kwargs))

    def redirect_to(self, name, *args, **kwargs):
        """Redirect to URI that corresponds to route name"""
        self.redirect(self.uri_for(name, *args, **kwargs))