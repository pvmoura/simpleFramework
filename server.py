#!/usr/bin/env python

import socket
import re

class Server(object):
	def __init__(self):
		self.s = socket.socket()
		self.s.bind(('', 8080))
		self.s.listen(5)
		self.response_dict = {
			"status": '200 OK',
			"version": "HTTP/1.1",
			"content-type": "text/plain",
		}

	def parse_route(self, route_string):
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


	def serve_requests(self):
		"""serve requests with responses"""
		while True:
			c, (addr, port) = self.s.accept()
			output = self.handle_request(c)
			if not output:
				output = self.build_response_headers({
						"status": '404 Not Found',
						"version": "HTTP/1.1",
						"content-type": "text/plain",
					})
				output += 'Bad request'
			c.send(output)
			c.close()

	def handle_request(self, c):
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
				method = method_list[0]
				route = self.parse_route(method_list[1])
				processed_headers = self.process_headers(listed_data)
				#send to application layer for output
			else:
				#get out
				pass		

			output = self.build_response_headers(self.response_dict)
			output += 'hello you there!'
			return output
		else:
			return False

	def build_response_headers(self, response_dict):
		""" Takes a header dictionary and build a string to send as response headers"""
		headers_string = response_dict['version'] + " " + response_dict['status']
		for key, val in response_dict.iteritems():
			headers_string += key + ': ' + val + '\r\n'
		headers_string += '\r\n\r\n'
		return headers_string

s = Server()
s.serve_requests()