#
# an album of photos
#
class Album:
	def __init__(self):
		self.creationTimestamp = None # Unix timestamp of year/month/day
		self.pathComponent = None # "2001/12/31/someSubalbum"
		self.title = None # "November 8"
		self.summary = None # "First day of school"
		self.description = None # caption of album, probably contains HTML
		self.children = [] # my photos