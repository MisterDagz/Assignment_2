import random
import string

def randomString(stringLength=20):
	letters = string.ascii_lowercase
	letters += "0123456789"

	return ''.join(random.choice(letters) for i in range(stringLength))

def checkcookie(auth, userid):
	if auth in cookies.keys():
		if cookies[auth]['username'] == userid:
			return True
		else:
			cookies[auth]['failurecount'] += 1
		if cookies[auth]['failurecount'] >=3:
			cookies.pop(auth, None)
	return False

