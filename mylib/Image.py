#
# a physical image
#
# a Photo object might have several of these:  one for full size and one for thumbnail
#
class Image:
	def __init__(self):
		self.url = None # URL to image, including 'http://'
		self.height = None # Actual physical height of image
		self.width = None # Actual physical width of image