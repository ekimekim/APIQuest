from flask import request
from app import app


chars = {}

@app.route('/char/<charname>', methods=['POST'])
def create(charname):
	if charname in chars:
		return "Character already exists", 409
	chars[charname] = Character(charname)
	return 'Character created', 201


@app.route('/char/<charname>')
def get(charname):
	if charname not in chars:
		return "Character not found", 404
	char = chars[charname]
	return char.to_json()


@app.route('/char/<charname>/<attr>')
def charattr(charname, attr):
	if attr in attrs + ops:
		ret = getattr(chars[charname], attr)
	if attr in ops:
		ret = ret()
	return dumps(ret)
