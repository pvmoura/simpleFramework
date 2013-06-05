#!/usr/bin/env python

class Request(object):
	def __init__(self, method = "GET", route = '/', headers = {}, get_vars = {}, body = None):
		self.method = method
		self.headers = headers
		self.route = route
		self.body = body
