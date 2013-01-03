from gevent.wsgi import HTTPServer

from app import app
import character

BIND = '0.0.0.0'
PORT = 5000

if __name__=='__main__':
	WSGIServer((BIND, PORT), app).serve_forever()
