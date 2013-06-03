#!/usr/bin/env python

from wsgiref.simple_server import make_server

PORT = 80
PREFIX = ''
"""class application:
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response

	def application(self, environ, start_response):
		status = '200 OK'
		response_headers = [('Content-type','text/plain')]
		start_response(status, response_headers)
		return ['<html>Hello world!</html>']
"""

def application(environ, start_response):
	response_body = ['%s: %s' % (key, value) for key,value in sorted(environ.items())]
	response_body = '\n'.join(response_body)
	status = '200 OK'
	response_headers = [('Content-Type', 'text/plain'),('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return response_body
httpd = make_server(
	'localhost',
	PORT,
	application
)

httpd.handle_request()