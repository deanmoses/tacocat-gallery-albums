from AlbumThumbnail import AlbumThumbnail
from AlbumException import AlbumException
from NotFoundException import NotFoundException
from ThumbnailNotFoundException import ThumbnailNotFoundException
from ValidationException import ValidationException

#
# An album contains photos and subalbums
#
class Album(object):
	#
	# Convert from children to photos and childAlbumThumbs
	#
	def convertChildren(self):
		if hasattr(self, 'children'):
			if len(self.pathComponent) <= 4:
				self.childAlbumThumbnails = self.children
			else:
				self.photos = self.children
				self.photoOrder = self.childrenOrder
				del self.childrenOrder
			
			del self.children
			
	#
	# Initialize
	#
	def __init__(self, initial_dict={}):
		self.creationTimestamp = None # Unix timestamp of year/month/day
		self.pathComponent = None # "2001/12/31/someSubalbum"
		self.title = None # "2001" or "November 8"
		self.summary = None # "First day of school"
		self.description = None # caption of album, probably contains HTML
		self.photoOrder = [] # order of my child photos like ['supper', 'bedtime']
		self.photos = {} # my child photos Photo objects in a dict {'supper' : Photo object}
		self.childAlbumThumbnails = {} # thumbnail info of my child albums
   		self.thumbnailUrl = None # full http:// url to the photo to use as my thumbnail
		self.sidebar = None # the HTML of the sidebar containing firsts (only on Year albums)
		
		for key, value in initial_dict.iteritems():
			setattr(self, key, value)
			
		self.convertChildren()

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
		
		# Verify that photos and photoOrder are in sync
		photoNames = self.photos.keys()
		for photoOrderName in self.photoOrder:
			if photoOrderName not in photoNames:
				raise ValidationException(self.pathComponent, 'photos', 'PhotoOrder contains photo %s, which is not in photos' % (photoOrderName))

		if len(self.photoOrder) != len(self.photos):
			raise ValidationException(self.pathComponent, 'photos', 'photos length (%s) is not same same as photo order length (%s)' % (len(self.photos), len(self.photoOrder)))
		
		# if I don't have a thumbnail, choose one now randomly
		if not self.thumbnailUrl and len(self.photos) > 0:
			self.thumbnailUrl = self.photos.itervalues().next().fullSizeImage.url
	
	#
	# True if I'm the root album
	#
	def isRootAlbum(self):
		return not self.pathComponent
		
	#
	# True if I'm a year album
	#
	def isYearAlbum(self):
		return len(self.pathComponent) == 4
	
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
	def getPhoto(self, photoPathComponent):
		# strip the .jpg, if any
		photoName = photoPathComponent.rsplit('.', 1)[0]
		try:
			return self.photos[photoName]
		except KeyError:
			raise NotFoundException('Photo not found: %s/%s' % (self.pathComponent, photoName))
		
	#
	# Update an existing Photo in the album
	#
	def updatePhoto(self, photo):
		# strip the .jpg, if any
		photoName = photo.pathComponent.rsplit('.', 1)[0]
		try:
			oldPhoto = self.photos[photoName]
			self.photos[photoName] = photo
		except KeyError:
			raise NotFoundException('Photo not found: %s/%s' % (self.pathComponent, photoName))

	#
	# Return AlbumThumbnail of the specified child album
	#
	def getChildAlbumThumbnail(self, childAlbumPath):
		try:
			thumb = self.childAlbumThumbnails[childAlbumPath]
			if not isinstance(thumb, AlbumThumbnail):
				raise AlbumException('%s: thumb is not instance of AlbumThumbnail, is instead: %s' % (self.pathComponent, type(thumb)))
			return thumb
		except KeyError:
			raise ThumbnailNotFoundException(self.pathComponent, childAlbumPath)

	#
	# Set the AlbumThumbnail of one of my child albums.
	# This should be called when adding or updating a child album.
	#
	def setChildAlbumThumbnail(self, albumThumbnail):
		self.childAlbumThumbnails[albumThumbnail.pathComponent] = albumThumbnail

	#
	# Remove the specified child album as one of my thumbnails
	# This should be called when deleting a child album.
	#
	def delChildAlbumThumbnail(self, childPathComponent):
		self.childAlbumThumbnails.pop(childPathComponent, None)
	
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