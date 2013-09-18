#
# a photo in an album
#
class Photo:
	
	#
	# Initialize blank Photo
	#
	def __init__(self):
		self.pathComponent = None # name of photo like 'juicy1.jpg'
		self.title = None # title of photo, usually comes from photo's HTML file
		self.description = None # caption of photo, probably contains HTML
		self.fullSizeImage = None # Image object
		
	#
	# Initialize from a dict, most likely from a JSON object
	#
	def __init__(self, initial_dict):
		for key in initial_dict:
		            setattr(self, key, initial_dict[key])