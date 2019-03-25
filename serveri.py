import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import os
import sys
import json

from datetime import datetime

#import database as db

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
STATIC_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'static'))
TEMPLATES_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'templates'))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", MainPageHandler),
                (r"/gnomed", GnomePageHandler),
                (r"/mafiaclient", MafiaPageHandler),
                (r"/chat_ws", ChatWebSocketHandler),
            ]

        settings = dict(
                template_path=TEMPLATES_DIRECTORY,
                static_path=STATIC_DIRECTORY,
                debug=True,
             )
        tornado.web.Application.__init__(self, handlers, **settings)



class BaseHandler(tornado.web.RequestHandler):
    pass

class MainPageHandler(BaseHandler):
    def get(self):
        self.render('main_page.html')

class MafiaPageHandler(BaseHandler):
    def get(self):
        self.render('mafiaclient.html')

class GnomePageHandler(BaseHandler):
    def get(self):
        self.render('gnomed.html',
        		width=self.get_argument('width'),
        		height=self.get_argument('height'),
       		)

player_sockets = []

class ChatWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New client")
        self.name = None
        if self not in player_sockets:
            player_sockets.append(self)

    def on_close(self):
        print("Client lost")
        while self in player_sockets:
            player_sockets.remove(self)

    def on_message(self, message):
        print(message)
        if message.startswith('name:'):
            self.name = message.split(':')[1]
        else:
            data = {'name': self.name, 'message': message, 'timestamp': str(datetime.now())}
            # for socket in player_sockets:
            #     if socket != self:
            #         socket.write_message(data)
            self.write_message(data)


def load_config_file(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print ("error: missing config file")
        exit(0)
    config = load_config_file(sys.argv[1])

    httpserver = tornado.httpserver.HTTPServer(Application())
    PORT = config['port']
    httpserver.listen(PORT)
    print("Server listening port {}".format(PORT))
    tornado.ioloop.IOLoop.current().start()


