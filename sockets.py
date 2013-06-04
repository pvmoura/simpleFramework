#!/usr/bin/env python

import socket
import re
class MessageReader(object):
	def __init__(self, socket):
		self.buffer = b''

	def get_bytes(self, new):
		"""while new not in self.buffer:
			if not self._fill():
				return b''"""



class Server(object):
	def __init__(self):
		self.s = socket.socket()
		self.s.bind(('', 8080))
		self.s.listen(5)

	def process_headers(self, data):
		listed_data = data.rstrip().split('\n')
		method = listed_data.pop(0).rstrip()
		headers = {}
		for i in range(len(listed_data)):
			listed_data[i] = listed_data[i].rstrip()
			splits = listed_data[i].split(": ")
			headers[splits[0]] = splits[1]
		return method, headers

	def serve_requests(self):
		while True:
			c, (addr, port) = self.s.accept()
			data = ""

			while True:
				rec_data = c.recv(256)
				if not rec_data: break
				data += rec_data
				if re.search('\r\n\r\n$', rec_data):
					break
			processed_data = self.process_headers(data)
			c.send('hello')
			c.close()

s = Server()
s.serve_requests()