from flask import request, g
from collections import namedtuple
from simplejson import dumps

from app import app

chars = {}

@app.route("/char/<charname>/move", methods=['POST'])
def movechar(charname):
	if charname not in chars:
		return "Character not found", 404
	char = chars[charname]
	direction = request.form['direction']
	if direction not in ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
		return "Bad direction.", 400
	direction = direction[0]
	if direction == 'n': char.position[1] += 1
	if direction == 's': char.position[1] -= 1
	if direction == 'e': char.position[0] += 1
	if direction == 'w': char.position[0] -= 1
	return 'Character moved'


if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)
