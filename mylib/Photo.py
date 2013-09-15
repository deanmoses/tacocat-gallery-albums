#
# a photo in an album
#
class Photo:
	def __init__(self):
		self.pathComponent = None # name of photo like 'juicy1.jpg'
		self.title = None # title of photo, usually comes from photo's HTML file
		self.description = None # caption of photo, probably contains HTML