import os
import jinja2
import cherrypy

try:
    from .model import Account, Question
except ImportError:
    from model import Account, Question

from sqlalchemy.sql import select, update, and_


__all__ = [
    "MainHandler",
    ]

dirname = os.path.join(os.path.dirname(__file__), "template")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(dirname))


class MainHandler:
    @staticmethod
    def render(src, **params):
        return jinja_env.get_template(src).render(params)
    
    @cherrypy.expose
    def index(self, **kwargs):
        return self.render("index.html")


if __name__ == "__main__":
    cherrypy.quickstart(MainHandler(), "/")
