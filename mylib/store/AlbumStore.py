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
#logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)

# import my own local code
from Config import Config
from album.Album import Album
from album.Photo import Photo
from album.YearAlbum import YearAlbum
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
		
		# get string of JSON from disk
		jsonString = fileUtils.readFile(albumFilePath)

		# turn into Album object
		album = jsonUtils.fromJson(jsonString)
		
		assert album, '%s: error retrieving album from store, it is null' % albumPath
		
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
		albumPathUtils.validatePath(photoPath)
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
		return AlbumStore.getAlbum(parentPath)
	
	#
	# Check if we need to update derived fields on parent album.
	#
	@staticmethod
	def __updateParent(album):
		# only need to do update the parent of day albums, not year or sub albums
		if not album.isDayAlbum(): return
		
		# retrieve parent album -- will be a year album
		parentAlbum = AlbumStore.getParentAlbum(album.pathComponent)
		assert isinstance(parentAlbum, YearAlbum), '%s: error checking if I need to update parent, it is not of type YearAlbum: %s' % (album.pathComponent, type(parentAlbum))
		
		# compare thumbnail previously saved in parent album
		thumbCurrent = album.toThumbnail()
		thumbOnParent = parentAlbum.getChildAlbumThumbnail(album.pathComponent)
		needsUpdating = (thumbOnParent != thumbCurrent)
		
		# update the parent
		if needsUpdating:
			print '''    Derived album thumbnail values differ.\nparent:  %s\ncurrent: %s\ndiffs:%s''' % (thumbOnParent, thumbCurrent, thumbCurrent.diff(thumbOnParent))
			parentAlbum.setChildAlbumThumbnail(thumbCurrent)
			AlbumStore.updateAlbum(parentAlbum)
		else:
			print '    Derived album thumbnail values are the same, not updating.'
		
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
		# raises exception if album has missing or invalid fields
		album.validate()

		# convert object into JSON string
		albumString = jsonUtils.toJson(album)
		
		# get full path to album's JSON file on disk
		albumFilePath = AlbumStore.__getAlbumFilePath(album.pathComponent)
		
		if Config.doWriteToDisk:
			# write to disk
			fileUtils.updateFile(albumFilePath, albumString)
			print '    Wrote to %s' % albumFilePath
		else:
			if Config.verbose:
				print albumString
			print '    Would have written to %s' % albumFilePath
		
		# check if we need to update derived fields on parent album
		AlbumStore.__updateParent(album)


	#
	# Instantiates but does not save an album
	#
	@staticmethod
	def newAlbum(albumPath, title, caption=None):
		# raise exception if path is invalid
		albumPathUtils.validatePath(albumPath)
		
		album = Album()
		album.pathComponent = albumPath
		album.title = title
		
		# album's created date is determined from the folder path, like "2001/12-31"
		pathParts = albumPath.split('/')
		monthDayParts = pathParts[1].split('-')
		yyyyMMdd = "%s/%s/%s" % (pathParts[0], monthDayParts[0], monthDayParts[1])
		album.creationTimestamp = int(time.mktime(datetime.datetime.strptime(yyyyMMdd, "%Y/%m/%d").timetuple()))
		
		return album
	
	#
	# Create new album with the specified path and write to the databse
	#
	@staticmethod
	def createAlbum(album):
		# get full path to album's JSON file on disk
		albumFilePath = AlbumStore.__getAlbumFilePath(album.pathComponent)
		
		if Config.doWriteToDisk:
			# write to disk
			fileUtils.createFile(albumFilePath, albumString)
			print '    Wrote to %s' % albumFilePath
		else:
			if Config.verbose:
				print albumString
			print '    Would have written to %s' % albumFilePath
		
		# check if we need to update derived fields on parent album
		AlbumStore.__updateParent(album)
		
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
		# retrieve photo's album from persistent store
		album = AlbumStore.getAlbum(albumPath)
		
		# set the updated photo object on it
		album.setPhoto(photo)
		
		AlbumStore.updateAlbum(album)
		
			
	#
	# Update the specified photo with the specified attributes
	# 
	@staticmethod
	def updatePhoto(photoPath, attributes):
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

		# update the photo's fields
		changed = False
		for key, newvalue in attributes.iteritems():
			oldvalue = getattr(photo, key)
			if oldvalue != newvalue:
				setattr(photo, key, newvalue)
				changed = True	

		# get path to album that the photo lives in
		albumPathUtils.validatePath(photoPath)
		pathParts = photoPath.split('/')
		photoName = pathParts.pop()
		parentAlbumPath = '/'.join(pathParts)
				
		# persist updated photo
		AlbumStore.updatePhoto(parentAlbumPath, photo)
		