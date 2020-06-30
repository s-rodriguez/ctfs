#!/usr/bin/env python3
import urllib
# NOOO! Alguien eliminó esto!
import %%%%%% as remolino

class Server:
	def __init__(self):
		...
		self.generate_mac_key()
		...

	def generate_mac_key(self):
		self.mac_key = b"Th1s1sS3cure4sH3ll" + os.urandom(14)

	def check_tag(self, tag, params):
		decoded_params = urllib.parse.unquote_to_bytes(params)
		return tag == remolino.new(self.mac_key+decoded_params).hexdigest()

	def parse_params(self, body):
		return dict(param_value.split("=") for param_value in body.split("&"))

	def serve_for_ever(self):
		...

	def doget(self, request):
		...

	def dopost(self, request):
		...
		ct = request.headers.get("Content-type")
		if not form_urlencoded(ct.lower()):
			return error()
		tag = request.headers.get("Tag")
		params = request.body()
		if self.check_tag(tag, params):
			params = parse_params(urllib.parse.unquote(params))
			if params['action'] == 'activate':
				activate_bomb()
			elif params['action'] == 'defuse':
				defuse_bomb()
			else:
				....
		else:
			return error()
		...
	...
server = Server()
server.serve_for_ever()
