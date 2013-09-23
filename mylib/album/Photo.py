from ValidationException import ValidationException

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
		
	#
	# Error if any of my fields are missing or invalid
	#
	def validate(self):
		# ensure required fields aren't missing or blank
		for fieldName in ['pathComponent', 'title', 'fullSizeImage']:
			if (not hasattr(self, fieldName)) or (not getattr(self, fieldName)):
				raise ValidationException(self.pathComponent, fieldName, "missing or blank")
		
		self.fullSizeImage.validate()
			
		