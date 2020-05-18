import os
import cherrypy

from .model import Model
from .view import MainHandler


class Server:
    SITE_CONF = {
        "server.socket_host": "localhost",
        "server.socket_port": 8080,
        "server.thread_pool": 100,
        "server.max_request_body_size": 50000000,
        "server.socket_timeout": 5,
        }

    def __init__(self, db_uri):
        Model.start_engine(db_uri)
        Model.initial_meta()

    def run(self):
        cherrypy.quickstart(MainHandler(), "/")


if __name__ == "__main__":
    server = Server()
    server.run()
