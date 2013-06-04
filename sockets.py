#!/usr/bin/env python

import socket
import re
class Router(object):
	def __init__(self):
		self.route = ""
		

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

		method_list = method.split(" ")
		request_dict = {
			"headers": headers
		}
		if len(method_list) == 3:
			request_dict["method"] = method_list[0]
			if re.search("\?", method_list[1]):
				request_dict["route"] = method_list[1].split("?").pop(0)
				request_dict["get_vars"] = {}
				for val in method_list[1].split("?")[1].split("&"):
					request_dict["get_vars"][val.split("=")[0]] = val.split("=")[1]

			else:
				request_dict["route"] = method_list[1]
			request_dict["type"] = method_list[2]
		else:
			request_dict["method"] = method_list

		return request_dict

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
			output = processed_data["method"]
			if type(output) is list:
				output = output[0]
			c.send(output)
			c.close()

s = Server()
s.serve_requests()