import tornado.ioloop
import tornado.web
import tornado.httpserver
import os
import sys
import json

#import database as db

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
STATIC_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'static'))
TEMPLATES_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'templates'))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", MainPageHandler),
                (r"/gnomed", GnomePageHandler),
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

class GnomePageHandler(BaseHandler):
    def get(self):
        self.render('gnomed.html',
        		width=self.get_argument('width'),
        		height=self.get_argument('height'),
       		)


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


