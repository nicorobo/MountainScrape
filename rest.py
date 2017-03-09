# rest.py

import json
import requests

def post(extension, data):
	headers = {'Content-Type': 'application/json'}
	data = json.dumps(data)
	r = requests.post("http://localhost:3000"+extension, data=data, headers=headers)
	# Returning the response
	return r