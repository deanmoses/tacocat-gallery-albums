#
# a photo in an album
#
class Photo(object):
	
	#
	# Initialize from a dict, most likely from a JSON object
	#
	def __init__(self, initial_dict={}):
		self.pathComponent = None # name of photo like 'juicy1.jpg'
		self.title = None # title of photo, usually comes from photo's HTML file
		self.description = None # caption of photo, probably contains HTML
		self.fullSizeImage = None # Image object
		
		for key in initial_dict:
			setattr(self, key, initial_dict[key])
			
	#
	# Python's built-in toString() method
	#
	def __str__(self):
		return str(self.__dict__)

	#
	# Python's built-in equality comparison
	#
	def __eq__(self, other): 
		return self.__dict__ == other.__dict__
