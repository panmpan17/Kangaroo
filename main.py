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
    def index(self, login_id=None):  # index = "/"
        if cherrypy.request.method == "GET":
            login_cookie = cherrypy.request.cookie.get("login_id")
            password_cookie = cherrypy.request.cookie.get("password")

            if login_cookie is not None:
                return self.render(
                    "index.html",
                    login_id=login_cookie.value)

            return self.render("index.html")
        
        elif cherrypy.request.method == "POST":
            cherrypy.response.cookie["login_id"] = login_id
            cherrypy.response.cookie["login_id"]["path"] = "/"
            cherrypy.response.cookie["login_id"]["max-age"] = 3600

            raise cherrypy.HTTPRedirect("/")
    
    @cherrypy.expose
    def logout(self):
        if "login_id" in cherrypy.request.cookie.keys():
            cherrypy.response.cookie["login_id"] = ""
            cherrypy.response.cookie["login_id"]["expires"] = 0
            print(cherrypy.response.cookie["login_id"])

        raise cherrypy.HTTPRedirect("/")
    
    @cherrypy.expose
    def login(self, **kwargs):
        cherrypy.response.cookie["test"] = "test"
        cherrypy.response.cookie["test"]["path"] = "/login"
        cherrypy.response.cookie["test"]["max-age"] = 3600
        return "Cookies!"

    @cherrypy.expose
    def url_al(self):
        return "url"


if __name__ == "__main__":
    cherrypy.quickstart(App(), "/", {
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(os.getcwd(), "server", "static"),
        }
    })
