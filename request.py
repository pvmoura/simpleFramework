#!/usr/bin/env python

class Request(object):
	def __init__(self, method = "GET", version = "HTTP/1.1", route = '/', headers = {}, get_vars = {}, body = None):
		self.method = method
		self.headers = headers
		self.route = route
		self.body = body
		self.version = version
