#!/usr/bin/env python

import socket
import re
from request import Request
from select import select
import datetime
import Queue

class Server(object):
	def __init__(self):
		self.s = socket.socket()
		self.s.bind(('', 8080))
		self.s.listen(5)
		self.readables, self.writeables = [self.s], []
		self.s.setblocking(0)
		self.message_queues = {}


	def parse_route(self, route_string):
		"""parses out the route and any get variables"""
		get_vars = {}
		if re.search("\?", route_string):
			route = route_string.split("?").pop(0)
			get_vars = {
				val.split("=")[0]: val.split("=")[1] for val in route_string.split("?")[1].split("&")
			}
		else:
			route = route_string
		return route, get_vars

	def process_headers(self, listed_data):
		"""takes a list of headers and turns it into a dictionary"""
		return {
			val.rstrip().split(": ")[0]: val.rstrip().split(": ")[1] for val in listed_data
		}


	def serve_requests(self, app):
		"""serve requests with responses"""
		while True:
			while self.readables:
				rs, ws, xs = select(self.readables, self.writeables, self.readables)

				for r in rs:
					if r is self.s:
						c, (addr, port) = self.s.accept()
						c.setblocking(0)
						self.readables.append(c)
						self.message_queues[c] = Queue.Queue()
					else:
						request = self.read_socket(r)
						if request:
							message_queues[r].put(request)
							if r not in self.writeables:
								self.writeables.append(r)
						else:
							if r in self.writeables:
								self.writeables.remove(r)
							self.readables.remove(r)
							r.close()
							del message_queues[r]

				for c in ws:
					try:
						msg = message_queues[c].get_nowait()
					except Queue.Empty:
						self.writeables.remove(c)
					else:
						output = self.handle_write(msg, app)
						c.send(output)
						self.writeables.remove(c)
						c.close()
				
				for x in xs:
					self.readables.remove(x)
					if x in self.writeables:
						self.writeables.remove(x)
					x.close()
					del message_queues[x]

	def read_socket(self, c):
		# take a raw socket and process the data into something that handle_write can understand
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
					method_list[2],
					parsed_route[0],
					self.process_headers(listed_data),
					parsed_route[1]
				)
			else:
				r = False
			return r
		else:
			return False


	def write_socket(self, request, app):
		# take a preprocessed python object and handle the writing
		app_response = app(request)
		if app_response:
			headers = self.build_response_headers(app_response['headers'])
			response = app_response['response']
		else:
			headers = self.build_response_headers({
				"status": '404 Not Found',
				"version": "HTTP/1.1",
				"content-type": "text/plain",
			})
			response = "Bad request"

		output = self.build_response_headers(headers)
		output += response
		return output

	def build_response_headers(self, response_dict):
		""" Takes a header dictionary and builds a string to send as response headers"""
		headers_string = response_dict['version'] + " " + response_dict['status']
		for key, val in response_dict.iteritems():
			headers_string += key + ': ' + val + '\r\n'
		headers_string += '\r\n'
		return headers_string