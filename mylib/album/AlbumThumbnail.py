#
# Info about an Album needed for its thumbnail on the parent album
#

# 3rd party libs
import copy

# my libs
from Image import Image

#
# Info about an Album needed for its thumbnail on the parent album
#
class AlbumThumbnail(object):
	
	#
	# Initialize 
	#
	# dict overrides Album object if both have
	# same field specified
	#
	def __init__(self, initial_dict={}, album=None):
		self.creationTimestamp = None # Unix timestamp of year/month/day
		self.pathComponent = None # "2001/12/31/someSubalbum"
		self.title = None # "November 8"
		self.summary = None # "First day of school"
		self.fullSizeImage = Image()
		
		if album:
			self.creationTimestamp = album.creationTimestamp
			self.pathComponent = album.pathComponent
			self.title = album.title
			self.summary = album.summary
			self.thumbnailUrl = album.thumbnailUrl
		
		for key in initial_dict:
			setattr(self, key, initial_dict[key])
			
		# description was saved on some old versions, remove it it
		if hasattr(self, 'description'):
			print 'removing description'
			del self.description
		
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
		
		return cmp(
			(self.creationTimestamp, self.pathComponent, self.title, self.summary, self.fullSizeImage),
			(other.creationTimestamp, other.pathComponent, other.title, other.summary, other.fullSizeImage)
		)
		
	#
	# get array of keys that are different between two AlbumThumbnails
	#
	def diff(self, other):
		diffs = []
		for key in dir(self):
			if not key.startswith('__') and not key == 'diff':
				myValue = getattr(self, key)
				otherValue = getattr(other, key)
				if myValue != otherValue:
					diffs.append(key)
		return diffs