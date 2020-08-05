import os
import jinja2
import cherrypy


dirname = os.path.join(os.path.dirname(__file__), "server/template")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(dirname))


class App:
    @staticmethod
    def render(src, **params):
        return jinja_env.get_template(src).render(params)

    @cherrypy.expose  # function 名字跟 URL 有關
    def index(self, **data):  # index = "/"
        if cherrypy.request.method == "GET":
            return self.render('index.html')
        
        elif cherrypy.request.method == "POST":
            return str(data)
    
    @cherrypy.expose
    def login(self, **kwargs):
        return cherrypy.request.method
        return str(kwargs)

    @cherrypy.expose
    def url_al(self):
        return "url"


if __name__ == "__main__":
    cherrypy.quickstart(App(), "/", {
        "/images": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(os.getcwd(), "server", "static"),
        }
    })
