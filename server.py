#!/usr/bin/env python

import socket
import re
from request import Request

class Server(object):
	def __init__(self):
		self.s = socket.socket()
		self.s.bind(('', 8080))
		self.s.listen(5)

	def parse_route(self, route_string):
		"""parses out the route and any get variables"""
		get_vars = {}
		if re.search("\?", route_string):
			route = route_string.split("?").pop(0)
			for val in route_string.split("?")[1].split("&"):
				get_vars[val.split("=")[0]] = val.split("=")[1]

		else:
			route = route_string
		return route, get_vars

	def process_headers(self, listed_data):
		"""takes a list of headers and turns it into a dictionary"""
		headers = {}
		for i in range(len(listed_data)):
			listed_data[i] = listed_data[i].rstrip()
			splits = listed_data[i].split(": ")
			headers[splits[0]] = splits[1]
		return headers


	def serve_requests(self, app):
		"""serve requests with responses"""
		while True:
			c, (addr, port) = self.s.accept()
			output = self.handle_request(c, app)
			if not output:
				output = self.build_response_headers({
						"status": '404 Not Found',
						"version": "HTTP/1.1",
						"content-type": "text/plain",
					})
				output += 'Bad request'
			c.send(output)
			c.close()

	def handle_request(self, c, app):
		"""read request using sockets and return a simple response"""
		data = ""
		while True:
			rec_data = c.recv(1024)
			if not rec_data: break
			data += rec_data
			if re.search('\r\n\r\n$', rec_data):
				break
		if rec_data:
			listed_data = data.rstrip().split('\n')
			method_list = listed_data.pop(0).rstrip().split(" ")
			if len(method_list) == 3:
				parsed_route = self.parse_route(method_list[1])
				r = Request(
					method_list[0],
					parsed_route[0],
					self.process_headers(listed_data),
					parsed_route[1]
				)
				version = method_list[2]
				app_response = app(r)
			else:
				#get out
				pass		

			output = self.build_response_headers(app_response['headers'])
			output += app_response['response']
			return output
		else:
			return False

	def build_response_headers(self, response_dict):
		""" Takes a header dictionary and builds a string to send as response headers"""
		headers_string = response_dict['version'] + " " + response_dict['status']
		for key, val in response_dict.iteritems():
			headers_string += key + ': ' + val + '\r\n'
		headers_string += '\r\n'
		return headers_string