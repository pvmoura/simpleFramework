#!/usr/bin/env python

from server import Server

def simple_output(request):
	output = {
		"headers": {
			"status": '200 OK',
			"version": "HTTP/1.1",
			"content-type": "text/plain",
		}
	}
	output["response"] = request.headers['User-Agent']
	return output
s = Server()
s.serve_requests(simple_output)