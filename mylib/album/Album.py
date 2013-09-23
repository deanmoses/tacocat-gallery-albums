# 3rd party libs
import sys

# my libs
from AlbumThumbnail import AlbumThumbnail
from NotFoundException import NotFoundException
from ValidationException import ValidationException

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
		self.thumbnailChild = None # name of child photo for the album thumbnail, like 'supper'
		
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
		
		# Verify that children and chidrenOrder are in sync
		childrenNames = self.children.keys()
		for childOrderName in self.childrenOrder:
			if childOrderName not in childrenNames:
				raise ValidationException(self.pathComponent, 'children', 'Children contains photo %s, which is not in childOrder' % (childOrderName))

		if len(self.childrenOrder) != len(self.children):
			raise ValidationException(self.pathComponent, 'children', 'childOrder length (%s) is not same same as children length (%s)' % (len(self.childrenOrder), len(self.children)))
		
		# todo: validate photos
	
	#
	# I'm not a year album
	#
	def isYearAlbum(self):
		return False
	
	#
	# True I'm a day album (not a year album, and not a subalbum under a day album)
	# so 2001/12-31 but NOT 2001/12-31/snuggery
	def isDayAlbum(self):
		return self.pathComponent.count('/') == 1
	
	#
	# True if I'm an album under a day album, like 2001/12-31/snuggery
	#
	def isSubAlbum(self):
		return self.pathComponent.count('/') > 1
		
	#
	# Return child Photo object
	#	
	def getPhoto(self, childPathComponent):
		# strip the .jpg, if any
		photoName = childPathComponent.rsplit('.', 1)[0]
		try:
			return self.children[photoName]
		except KeyError:
			raise NotFoundException('Photo not found: %s/%s' % (self.pathComponent, photoName))
		
		
	#
	# Update an existing Photo in the album
	#
	def updatePhoto(self, photo):
		# strip the .jpg, if any
		photoName = photo.pathComponent.rsplit('.', 1)[0]
		try:
			oldPhoto = self.children[photoName]
			self.children[photoName] = photo
		except KeyError:
			raise NotFoundException('Photo not found: %s/%s' % (self.pathComponent, photoName))
	
	#
	# Set the name of the child photo to be used as the album thumbnail
	#
	def setAlbumThumbnailPhoto(self, childName):
		assert childName in self.children, 'Thumbnail %s is not in children %s' % (childName, self.children)
		self.thumbnailChild = childName
	
	#
	# Return child Photo object that is the album thumbnail
	# or None if not yet set
	#
	def getAlbumThumbnailPhoto(self):
		if self.thumbnailChild: 
			return self.children[self.thumbnailChild]
		else: 
			return None
		
	#
	# Make a copy of myself with a smaller set of fields, just
	# the stuff needed for my parent album to create a thumbnail
	#
	def toThumbnail(self):
		return AlbumThumbnail(album=self)
		
	#
	# Python's built-in toString() method
	#
	def __str__(self):
		return str(self.__dict__)

	#
	# Python's built-in equality comparison
	#
	def __eq__(self, other):
		if type(other) is dict:
			return self.__dict__ == other
		else:
			return self.__dict__ == other.__dict__