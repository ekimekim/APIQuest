from functools import wraps
from flask import request, session
from uuid import uuid4


AUTH_NEEDED = ("You must be logged in, and not be using a guest account.", 401,
               {'WWW-Authenticate': 'Basic realm="APIQuest"'})
AUTH_FAILED = ("Incorrect username or password.", 401,
               {'WWW-Authenticate': 'Basic realm="APIQuest"'})


def with_user(guest=True):
	"""Returns a decorator that wraps a function, examines the request for auth,
	and passes the resulting user to the function as the first arg.
	If guest=True, the user may use a guest account. If guest=False, a 401 is returned instead.

	Guest accounts:
		If the user has no auth, we create a temporary guest user, and save it to the session cookie.
		This guest session will then be used.
		Later, a special call can turn the current guest user into a real user.
		Guest users will be cleaned up after some timeout.

	Currently, this function tries to determine user using Basic Auth, or flask sessions.
	TODO require SSL on these pages.
	"""
	def _with_user(fn):
		@wraps(fn)
		def wrapped(*args, **kwargs):
			auth = request.authorization
			if auth:
				user = auth.username
				if not check_auth(auth.username, auth.password):
					return AUTH_FAILED
				session['user'] = user
			elif 'user' in session:
				user = session['user']
				if not guest and is_guest(user):
					return AUTH_NEEDED
			elif guest:
				user = uuid4()
				create_user(user, guest=True)
				session['user'] = user
			else:
				return AUTH_NEEDED
			return fn(user, *args, **kwargs)
		return wrapped
	return _with_user


def check_auth(user, password):
	"""TODO: Check user/password is correct.
	note to self: https://github.com/maxcountryman/flask-bcrypt
	"""
	return True


def create_user(user, guest=False):
	pass # TODO

def is_guest(user):
	return False # TODO
