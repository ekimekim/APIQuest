from uuid import uuid4
import gevent.queue
import gevent.event
from collections import defaultdict
from flask import request, abort


class Exposed(object):
	"""Indicates an attribute is to be exposed via the API.
	DO NOT set this attribute at the class level of an inheriting class.

	API is as follows:
		GET <entity url>: Returned JSON object contains attr=value
		GET <entity url>/attr: Return value as JSON.
	If not readonly:
		PUT <entity url>: If attr in form data, sets attr to value from form data
		PUT <entity url>/attr: Set attr to value of key "value" in form data
		POST: As PUT.

	Usage:
		class Example(object):
			foo = Exposed()
			bar = Exposed('baz', readonly=False)

	Usage with inheritance
	BAD:
		class Example2(Example):
			foo = '123'
	GOOD:
		class Example2(Example):
			def __init__(self):
				self.foo = '123'
	"""
	def __init__(self, value=None, readonly=True):
		# TODO add auth kwarg as per operation
		self.readonly = readonly
		self.values = defaultdict(lambda: value)
	def __get__(self, instance, owner):
		if instance is None: return self
		return self.values[instance]
	def __set__(self, instance, value):
		self.values[instance] = value


def operation(methods='POST', auth='OWNER'):
	"""Indicates a method is to be exposed via the API.
	Note that overriding this method in an inherited class will make it not exposed,
	unless you also declare that method exposed.

	The method is called when <entity url>/attr is requested with one of the HTTP methods
	listed by the methods kwarg, which must be either a string (single method) or iterable of strings.

	The method is called with kwargs from the request form data, and any TypeError will be transformed to a 400.
	Hence, you may take required args normally, and everything will happen properly.

	It requires auth as per the auth kwarg, as follows:
		auth='OWNER': Must be the entity controller to use this method.
		auth='ANY': Method may be called by any user (and may implement further checks itself)
		auth='NONE': Method does not require any auth. No user info is gathered.

	Is stackable, eg:
		@operation(methods='POST', auth='OWNER')
		@operation(methods='GET', auth='ANY')

	Example:
		class Example(object):
			@operation(methods='GET')
			def get_with_foo(foo, bar=None):
				# foo is required form arg, bar is optional. Any other form args present will cause a 400.
				...
	"""
	if isinstance(methods, str): methods = (methods,)
	def _operation(fn):
		if not fn._operation_info: fn._operation_info = []
		fn._operation_info.append((methods, auth))
	return _operation


class Entity(object):
	id = None
	controller = None # None indicates natural or "NPC"
	position = Exposed()
	image = Exposed()

	def __init__(self):
		self.id = uuid4()

	def _handle_route(url_part):
		"""Called by things that reference this entity.
		url_part should be the remainder of the url after the entity reference, without a leading slash."""
		if not url_part:
			# TODO GET dict of all exposed or POST/PUT updated values
			# for sake of non-repeated code, may be simpler to split gets and puts to call this func again with url_part=attr.
		else:
			parts = url_part.split('/')
			attr = parts[0]
			remainder = parts[1:]
			if isinstance(getattr(self.__class__, attr), Exposed):
				# TODO check auth
				# TODO if value is Entity, recurse.
				# TODO check readonly against method
				# TODO get or set value.
			elif hasattr(getattr(self.__class__, attr), '_operation_info'):
				if remainder: abort(404)
				# TODO check auth and method, call with **request.form
			else:
				abort(404)

	@property
	def exposed(self):
		"""Returns dict {exposed attrs: values}"""
		resolved = {}
		for cls in self.__class__.__mro__[::-1]:
			resolved.update(cls.__dict__)
		resolved.update(self.__dict__)
		ret = {}
		for k, v in resolved.items():
			if isinstance(v, Exposed):
				ret[k] = v
		return ret
