#
# a physical image
#
# a Photo object might have several of these:  one for full size and one for thumbnail
#
class Image(object):
	
	#
	# Initialize from a dict, most likely from a JSON object
	#
	def __init__(self, initial_dict={}):
		self.url = None # URL to image, including 'http://'
		self.height = None # Actual physical height of image
		self.width = None # Actual physical width of image
		
		for key in initial_dict:
			setattr(self, key, initial_dict[key])

	#
	# Python's built-in toString() method
	#
	def __str__(self):
		return str(self.__dict__)
		
	#
	# Python's built-in comparison operator
	# This is also called by __eq__ __ne__ __lt__ and __gt__
	#
	def __cmp__(self, other):
		#return self.__dict__ == other.__dict__
		
		if type(other) is dict:
			return self.__dict__ == other
		else:
			return cmp(
				(self.url, self.height, self.width),
				(other.url, other.height, other.width)
			)