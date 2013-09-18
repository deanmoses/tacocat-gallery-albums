#
# an album of photos
#
class Album(object):
	
	#
	# Initialize from a dict, most likely from a JSON object
	#
	def __init__(self, initial_dict={}):
		self.creationTimestamp = None # Unix timestamp of year/month/day
		self.pathComponent = None # "2001/12/31/someSubalbum"
		self.title = None # "November 8"
		self.summary = None # "First day of school"
		self.description = None # caption of album, probably contains HTML
		self.childrenOrder = [] # order of my child photos like ['supper', 'bedtime']
		self.children = {} # my child photos Photo objects in a dict {'supper' : Photo object}
		
		for key in initial_dict:
			setattr(self, key, initial_dict[key])
