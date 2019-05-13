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
    def __init__(self, config):
        handlers = [
                (r"/", MainPageHandler),
                (r"/gnomed", GnomePageHandler),
                (r"/mafiaclient", MafiaPageHandler),
                (r"/chat_ws", ChatWebSocketHandler),
                (r"/logout", LogoutHandler),
            ]

        self.config = config

        settings = dict(
                template_path=TEMPLATES_DIRECTORY,
                static_path=STATIC_DIRECTORY,
                debug=True,
                cookie_secret="askjdhaskjdahk",
             )
        tornado.web.Application.__init__(self, handlers, **settings)



class BaseHandler(tornado.web.RequestHandler):
    pass

class MainPageHandler(BaseHandler):
    def get(self):
        self.render('main_page.html',
                base_url="" if 'base_url' not in config else config['base_url'],
            )

class MafiaPageHandler(BaseHandler):
    def get(self):
        username = self.get_secure_cookie('user')
        if not username:
            self.render('mafiaclient_login.html')
        else:
            self.render_game()


    def post(self):
        username = self.get_argument('username')
        self.set_secure_cookie('user', username)
        self.render_game()

    def render_game(self):
        username = self.get_secure_cookie('user')
        self.render('mafiaclient.html',
                username=username,
            )

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('mafiaclient')




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
            data = {'name': self.name, 'message': message, 'timestamp': str(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))}
            for socket in player_sockets:
                if socket != self:
                    socket.write_message(data)
            self.write_message(json.dumps(data))


def load_config_file(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print ("error: missing config file")
        exit(0)
    config = load_config_file(sys.argv[1])

    httpserver = tornado.httpserver.HTTPServer(Application(config))
    PORT = config['port']
    httpserver.listen(PORT)
    print("Server listening port {}".format(PORT))
    tornado.ioloop.IOLoop.current().start()


