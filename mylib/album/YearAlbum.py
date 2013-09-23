from AlbumThumbnail import AlbumThumbnail
from NotFoundException import NotFoundException
from ThumbnailNotFoundException import ThumbnailNotFoundException
from AlbumException import AlbumException

#
# An album representing a year's worth of albums
#
class YearAlbum(object):
	
	#
	# Initialize from a dict, most likely from a JSON object
	#
	def __init__(self, initial_dict={}):
		self.creationTimestamp = None # Unix timestamp of year
		self.pathComponent = None # "2001
		self.title = None # "2001"
		self.children = {} # my child albums in a dict {'2001/12-31' : Album object}
		self.sidebar = None
		
		for key in initial_dict:
			setattr(self, key, initial_dict[key])
	
	#
	# Raises ValidationException if I have missing or invalid fields
	#
	def validate(self):
		# ensure required fields aren't blank
		for fieldName in ['creationTimestamp', 'pathComponent', 'title']:
			if (not hasattr(self, fieldName)) or (not getattr(self, fieldName)):
				raise ValidationException(self.pathComponent, fieldName, "missing")
		
		if not int(self.creationTimestamp):
			raise ValidationException(self.pathComponent, 'creationTimestamp', "not an integer")
		
		
	#
	# I'm a year album
	#
	def isYearAlbum(self):
		return True
	
	#
	# I'm not a day album, such as 2001/12-31 but NOT 2001/12-31/snuggery
	def isDayAlbum(self):
		return False
	
	#
	# I'm not an album under a day album, like 2001/12-31/snuggery
	#
	def isSubAlbum(self):
		return False
	
	#
	# Year albums don't contain photos
	#
	def getPhoto(photoName):
		raise NotFoundException('Year albums do not contain photos')
	
	#
	# Clone myself with a smaller set of fields, just
	# the stuff needed for the root album to create a thumbnail
	#
	def toThumbnail(self):
		return AlbumThumbnail(self)
		
	#
	# Return AlbumThumbnail of one of my child albums
	#	
	def getChildAlbumThumbnail(self, childPath):
		try:
			thumb = self.children[childPath]
			if not isinstance(thumb, AlbumThumbnail):
				raise AlbumException('%s: thumb is not instance of AlbumThumbnail, is instead: %s' % (self.pathComponent, type(thumb)))
			return thumb
		except KeyError:
			raise ThumbnailNotFoundException(self.pathComponent, childPath)
	
	#
	# Set the AlbumThumbnail of one of my child albums
	#
	def setChildAlbumThumbnail(self, albumThumbnail):
		self.children[albumThumbnail.pathComponent] = albumThumbnail
	
	#
	# Remove the specified child album as one of my thumbnails
	#
	def delChildAlbumThumbnail(self, childPath):
		self.children.pop(childPath, None)

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