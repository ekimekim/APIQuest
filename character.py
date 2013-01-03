from flask import request, abort
from app import app
from simplejson import dumps

chars = {}

@app.route('/char/<charname>', methods=['POST'])
def create(charname):
	if charname in chars:
		return "Character already exists\n", 409
	chars[charname] = Character(charname)
	return 'Character created\n', 201


@app.route('/char/<charname>')
def get(charname):
	if charname not in chars:
		return "Character not found\n", 404
	char = chars[charname]
	return char.to_json() + '\n'


class Character(object):
	attrs = set(['name', 'position', 'x', 'y']) # Names that are externally readable
	ops = {
		'GET': set([]),
		'POST': set(['move']),
	} # Names that are externally callable

	def __init__(self, name):
		self.name = name
		self.position = [0, 0]

	x = property(lambda self: self.position[0])
	y = property(lambda self: self.position[1])

	@x.setter
	def x(self, value):
		self.position[0] = value
	@y.setter
	def y(self, value):
		self.position[1] = value

	def to_json(self):
		return dumps(dict((attr, getattr(self, attr)) for attr in self.attrs), indent=4)

	def _move(self, x, y):
		"""Does the actual move, including any checks for whether its allowed."""
		self.x += x
		self.y += y

	# Operations

	def move(self, direction):
		DIRECTIONS = dict(
			northeast=(-1, 1), north=( 0, 1), northwest=( 1, 1),
			     east=(-1, 0),                     west=( 1, 0),
			southeast=(-1,-1), south=( 0,-1), southwest=( 1,-1))
		SHORTCUTS = dict(ne='northeast', n='north', nw='northwest',
		                  e='east'     ,             w='west',
		                 se='southeast', s='south', sw='southwest')
		direction = direction.lower()
		if direction in SHORTCUTS: direction = SHORTCUTS[direction]
		if direction not in DIRECTIONS:
			return "Bad direction. Direction must be one of:\n%s" % \
				'\n'.join(DIRECTIONS.keys() + SHORTCUTS.keys()), 400
		direction = DIRECTIONS[direction]
		return self._move(*direction)


@app.route('/char/<charname>/<attr>', methods=Character.ops.keys())
def charattr(charname, attr):
	if attr in Character.attrs + Character.ops[request.method]:
		if charname not in chars:
			return "Character not found\n", 404
		ret = getattr(chars[charname], attr)
	else:
		abort(404)
	if attr in Character.ops[request.method]:
		try:
			ret = ret(**request.form)
		except TypeError:
			abort(400)
	return dumps(ret)
