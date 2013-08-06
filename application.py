#!/usr/bin/env python

from server import Server

def simple_output(request):
	output = {}
	output['headers'] = {
		"status": '200 OK',
		"version": "HTTP/1.1",
		"content-type": "text/html",
	}
	output["response"] = '<html><head></head><form action="/" method="POST"><input type=text /><input type=submit value=Submit /></form></html>'
	return output

if __name__ == "__main__":
	s = Server()
	s.serve_requests(simple_output)