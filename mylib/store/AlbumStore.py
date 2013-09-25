#
# A persistent store of Albums and Photos
#

# import third party libraries
import glob
import os
import sys
import time
import datetime
import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

# import my own local code
from Config import Config
from album.Album import Album
from album.Photo import Photo
from album.AlbumException import AlbumException
from album.FoundException import FoundException
from album.NotFoundException import NotFoundException
import album.albumPathUtils as albumPathUtils
import fileUtils
import jsonUtils 

class AlbumStore(object):
	
	# static class variable that caches Albums to reduce disk reads
	# Album path (like '2001/12-31') -> Album object
	__store = {}
	
	def __init__(self):
		# do nothing
		pass

	#
	# Full path to album JSON file
	#
	@staticmethod
	def __getAlbumFilePath(albumPath):
		'''
		Return full path to album JSON file on disk

		Parameters
		----------
		albumPath : string
			path of album, like '2005' or '2005/12-31'

		Return
		----------
		Full path to album JSON file on disk
		'''
		# null or blank albumPath = root
		if not albumPath:
			return '%salbum.json' % (Config.outDir)
		else:
			return '%s%s/album.json' % (Config.outDir, albumPath)
	
	#
	# Retrieve album from persistent store
	#
	@staticmethod
	def getAlbum(albumPath):
		'''
		Retrieve album from persistent store.

		Parameters
		----------
		albumPath : string
			path of album, like '2005' or '2005/12-31'

		Return
		----------
		Album object
		
		Exception
		-----------
		Raises a NotFoundException if it can't find the album
		Raises an Exception if the retrieve fails for any reason.
		'''
		
		# attempt to retrieve album from cache
		if albumPath in AlbumStore.__store:
			logger.debug('%s: returning from cache', albumPath)
			return AlbumStore.__store[albumPath]
		else:
			logger.debug('%s: not found in cache', albumPath)
			
		# get full path to album's JSON file on disk
		albumFilePath = AlbumStore.__getAlbumFilePath(albumPath)
		
		# if album doesn't exist on disk, return None
		if not os.path.exists(albumFilePath):
			raise NotFoundException('Album %s not found' % albumFilePath)
			
		logger.debug('getAlbum(): reading from disk: %s' % albumFilePath)
		
		# get string of JSON from disk
		jsonString = fileUtils.readFile(albumFilePath)

		# turn into Album object
		album = jsonUtils.fromJson(jsonString)
		
		if not album:
			raise AlbumException('%s: error retrieving album from store, it is null' % albumPath)
		
		# put album in cache
		AlbumStore.__store[albumPath] = album

		return album
		
	#
	# Get photo
	#
	@staticmethod
	def getPhoto(photoPath):
		'''
		Retrieve photo from persistent store.

		Parameters
		----------
		path : string
			path to photo including album, like:
			'2005/12-31/harriet'
			'2005/12-31/snuggery/harriet'

		Return
		----------
		Photo object
		
		Exception
		-----------
		Raises a NotFoundException if it can't find the photo
		Raises an Exception if the retrieve fails for any reason.
		'''
		# get path to album that the photo lives in
		albumPathUtils.validatePhotoPath(photoPath)
		pathParts = photoPath.split('/')
		photoName = pathParts.pop()
		parentAlbumPath = '/'.join(pathParts)

		# retrieve the album
		album = AlbumStore.getAlbum(parentAlbumPath)
		
		# retrieve the photo from the album
		return album.getPhoto(photoName)
		
	#
	# Get parent album of specified album
	#
	@staticmethod
	def getParentAlbum(albumPath):
		parentPath = albumPathUtils.parentPathFromChildPath(albumPath)
		logger.debug('getParentAlbum(%s): parent path is: %s' % (albumPath, parentPath))
		return AlbumStore.getAlbum(parentPath)
	
	#
	# Check if we need to update derived fields on parent album.
	#
	@staticmethod
	def __updateParent(album, create=False):
		'''
		Parameters
		----------
		create: boolean
			True: the child album is new, a thumb should not already exist.
			False: the child album already exists, its thumb should already exist.
		'''
		# don't need to update the nonexistent parent of the root album
		if album.isRootAlbum(): return
		
		# retrieve parent album
		parentAlbum = AlbumStore.getParentAlbum(album.pathComponent)
		
		# what we're saving to parent
		thumbCurrent = album.toThumbnail()
		
		# compare to previously saved thumbnail to
		# see if the values have actually changed
		needsUpdating = create or (thumbCurrent != parentAlbum.getChildAlbumThumbnail(album.pathComponent))

		# update the parent
		if needsUpdating:
			parentAlbum.setChildAlbumThumbnail(thumbCurrent)
			AlbumStore.updateAlbum(parentAlbum)
			logger.debug('%s: updated thumbnail for child: %s', parentAlbum.pathComponent, album.pathComponent)
		else:
			logger.debug('%s: derived album thumbnail values are the same, not updating.', parentAlbum.pathComponent)
	
	@staticmethod
	def __saveAlbum(album, create=False):
		'''
		Parameters
		----------
		create: boolean
			True: save new album. Fails if album already exists.
			False: update existing album. Fails if album doesn't already exist.
		'''
		# raises exception if album has missing or invalid fields
		album.validate()
		
		# convert album object into JSON string
		albumString = jsonUtils.toJson(album)
		
		# get full path to album's JSON file on disk
		albumFilePath = AlbumStore.__getAlbumFilePath(album.pathComponent)
		
		# write to disk
		if create:
			try:
				fileUtils.createFile(albumFilePath, albumString)
			except AssertionError:
				raise FoundException(album.pathComponent)
		else:
			try:
				fileUtils.updateFile(albumFilePath, albumString)
			except AssertionError:
				raise NotFoundException(album.pathComponent)
			
		logger.debug('Wrote to %s', albumFilePath)
			
		# put / update album in cache
		AlbumStore.__store[album.pathComponent] = album
		
		# create or update my thumbnail on parent album, if needed
		AlbumStore.__updateParent(album, create)
		
		
	#
	# Create new album with the specified path and write to the databse
	#
	@staticmethod
	def createAlbum(album):
		AlbumStore.__saveAlbum(album, create=True)
			
	#
	# Update existing album in persistent store
	#
	@staticmethod
	def updateAlbum(album):
		'''
		Update existing album in persistent store, updating any parent album as needed,
		such as parentAlbum.children.title.

		Parameters
		----------
		album : Album
			album object to update

		Exception
		-----------
		Raises an exception if the update fails for any reason.
		'''
		AlbumStore.__saveAlbum(album)

	#
	# Instantiates but does not save a year album
	#
	@staticmethod
	def __newYearAlbum(year):
		yearInt = int(year)
		assert  yearInt > 1800 and yearInt < 2200
		
		album = YearAlbum()
		album.title = year
		album.pathComponent = year
		
		# set timestamp to Jan 1 of the year
		album.creationTimestamp = int(time.mktime(datetime.datetime(year=yearInt, month=1, day=1).timetuple()))
		
		return album
		
	
	#
	# Instantiates but does not save an album
	#
	@staticmethod
	def newAlbum(albumPath, title=None, description=None):
		# raise exception if path is invalid
		pathParts = albumPathUtils.parsePath(albumPath)
		
		# if the path is just a year, create new year album
		if (len(pathParts) == 1):
			if title or description:
				raise AlbumException('Cannot create year album with title or description')
			return AlbumStore.__newYearAlbum(pathParts[0])
		
		# else create new day album
		album = Album()
		album.pathComponent = albumPath
		album.description = description
		
		# album's created date is determined from the folder path, like "2001/12-31"
		pathParts = albumPath.split('/')
		monthDayParts = pathParts[1].split('-')
		yyyyMMdd = "%s/%s/%s" % (pathParts[0], monthDayParts[0], monthDayParts[1])
		album.creationTimestamp = int(time.mktime(datetime.datetime.strptime(yyyyMMdd, "%Y/%m/%d").timetuple()))
		
		if title:
			album.title = title
		else:
			# long format day, like "December 1".  No year.
			album.title = datetime.datetime.fromtimestamp(album.creationTimestamp).strftime('%B %-d')
		
		return album
	
	#
	# Update the specified photo 
	#
	@staticmethod
	def updatePhoto(albumPath, photo):
		'''
		Updates a photo already in the persistent store.

		Parameters
		----------
		path : string
			full path to the ALBUM that the photo lives in, 
			'2001/12-31'
			'2001/12-31/snuggery'

		photo : Photo
			the photo object to update
			
		Exception
		-----------
		Raises an exception if the update fails for any reason.
		'''
		logger.debug('updatePhoto(%s) albumPath: %s' % (photo.pathComponent, albumPath))
		
		# retrieve photo's album from persistent store
		album = AlbumStore.getAlbum(albumPath)
		
		logger.debug('updatePhoto(%s) got album: %s' % (photo.pathComponent, album.pathComponent))
		
		# update existing photo in the album
		album.updatePhoto(photo)
		
		AlbumStore.updateAlbum(album)
		
			
	#
	# Update the specified photo with the specified attributes
	# 
	@staticmethod
	def updatePhotoFromDict(photoPath, attributes):
		'''
		Updates a photo already in the persistent store.

		Parameters
		----------
		photoPath : string
			full path to photo like 
			'2001/12-31/felix'
			'2001/12-31/felix.jpg'

		attributes : dict
			dict of attributes to update
			
		Exception
		-----------
		Raises an exception if the attributes dict contains
		keys that aren't valid photo attributes.
		
		Raises an exception if the update fails for any reason.
		'''
		# retrieve photo from persistent store
		photo = AlbumStore.getPhoto(photoPath)
		
		logger.debug('updatePhoto(%s)' % photoPath)

		# update the photo's fields
		changed = False
		for key, newvalue in attributes.iteritems():
			oldvalue = getattr(photo, key)
			if oldvalue != newvalue:
				setattr(photo, key, newvalue)
				changed = True	

		if not changed:
			logger.debug('updatePhotoFromDict(%s): nothing changed, not resaving' % photoPath)
			
		# validate the changed photo
		photo.validate()
		
		# get path to album that the photo lives in
		albumPathUtils.validatePath(photoPath)
		pathParts = photoPath.split('/')
		photoName = pathParts.pop()
		parentAlbumPath = '/'.join(pathParts)
		
		logger.debug('updatePhoto(%s): parent path: %s' % (photoPath, parentAlbumPath))
				
		# persist updated photo
		AlbumStore.updatePhoto(parentAlbumPath, photo)
	
		
	#
	# Delete album at the specified path
	#
	@staticmethod
	def deleteAlbum(albumPath):
		# raise exception if path is invalid
		albumPathUtils.validatePath(albumPath)
		
		# get full path to album's JSON file on disk
		albumFilePath = AlbumStore.__getAlbumFilePath(albumPath)
		
		# if album doesn't exist on disk, return None
		if not os.path.exists(albumFilePath):
			raise NotFoundException('Album not found: %s' % albumFilePath)
		
		# delete album from disk
		fileUtils.deleteFile(albumFilePath)
		
		# remove album from cache
		AlbumStore.__store.pop(albumPath, None)
		
		# remove deleted album's thumbnail info from parent album
		parentAlbum = AlbumStore.getParentAlbum(albumPath)
		parentAlbum.delChildAlbumThumbnail(albumPath)
		AlbumStore.updateAlbum(parentAlbum)
		