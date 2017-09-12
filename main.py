#coding: utf-8
from gevent.wsgi import WSGIServer
from index import app

http_server = WSGIServer(('', 5098), app)
http_server.serve_forever()
# import os
# import gevent.monkey
# gevent.monkey.patch_all()
#
# import multiprocessing
#
# bind = '0.0.0.0:5058'
# # pidfile = 'log/gunicorn.pid'
# # logfile = 'log/debug.log'
#
# #启动的进程数
# workers = multiprocessing.cpu_count() * 2 + 1
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'
#
# x_forwarded_for_header = 'X-FORWARDED-FOR'
# from gevent.wsgi import WSGIServer
# from index import app
# http_server = WSGIServer(('', 5058), app)
# http_server.serve_forever()
# from tornado.wsgi import WSGIContainer
# from tornado.httpserver import HTTPServer
# from tornado.ioloop import IOLoop
# from index import app
#
# from tornado.options import options
#
#
# if __name__ == '__main__':
#
#     args = options.parse_command_line()
#     if len(args) == 0:
#         port = 5058
#     else:
#         port = args[0]
#
#
#     http_server = HTTPServer(WSGIContainer(app), xheaders=True)
#
#     http_server.listen(port)
#     IOLoop.instance().start()
