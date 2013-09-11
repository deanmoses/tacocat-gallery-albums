#
# a photo in an album
#
class Photo:
	def __init__(self):
		self.name = None # name of photo like 'juicy1'
		self.title = None # title of photo, usually comes from photo's HTML file
		self.caption = None # caption of photo, probably contains HTML
		self.imageFile = None # full path to full sized photo jpg starting with /home/deanmoses/