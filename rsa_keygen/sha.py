import hashlib

def digst(string):
	d = hashlib.sha1(string.encode()).hexdigest()
	return d
