#!/bin/env python
# coding=utf-8
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

import tornado.options
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.auth
import tornado.locale
from tornado import gen
from tornado.escape import json_encode, json_decode

from controller import tool_video
from controller import tool_article

from setting import settings


class MainHandler(tornado.web.RequestHandler):
    def get(self, app):
        self.write("Hello, world")


class CleanCacheAPIHandler(tornado.web.RequestHandler):
    def get(self):
        t = self.get_argument('t', None)
        os.system('python3 ' + os.path.join(os.path.dirname(__file__), 'Clean_cache.py'))
        self.finish({'info': "ok"})


class MakeVideoAPIHandler(tornado.web.RequestHandler):
    def get(self):
        t = self.get_argument('t', None)
        os.system('python3 ' + os.path.join(os.path.dirname(__file__), 'make_video.py'))
        self.finish({'info': "ok"})

application = tornado.web.Application([
    (r"/demo/article", tool_article.ArticleDemoHandler),
    (r"/demo/video", tool_video.VideoDemoHandler),
    (r"/api/tool/article/CleanCache", CleanCacheAPIHandler),
    (r"/api/tool/article/MakeVideo", MakeVideoAPIHandler),
    (r"/api/tool/video/get_one", tool_video.GetVideoOneAPIHandler),
    # (r"/api/tool/article/make_video",tool_article.MakeVideoArticleAPIHandler),
    (r"/api/tool/article/get_info", tool_article.GetArticleInfoAPIHandler),
    (r"/api/tool/article/get_json", tool_article.GetArticleJsonAPIHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/(.*)", MainHandler),
], **settings)

if __name__ == "__main__":
    tornado.options.define("port", default=8001, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()
    application_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    application_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

