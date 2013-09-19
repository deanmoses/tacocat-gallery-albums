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

# import my own local code
from Config import Config
from Album import Album
from Photo import Photo
from YearAlbum import YearAlbum
import albumPathUtils
import toFile
import toJson 

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
	def getAlbum(albumPath, errorIfNotFound=False):
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
		Raises an exception if the retrieve fails for any reason.
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
			if errorIfNotFound:
				raise Exception('Album %s not found on disk' % albumFilePath)
			else:
				logger.warn('%s: not found on disk at file path', albumPath, albumFilePath)
				return None
		
		# get string of JSON from disk
		jsonString = toFile.fromFile(albumFilePath)

		# turn into Album object
		album = toJson.fromJson(jsonString)
		
		assert album, '%s: error retrieving album from store, it is null' % albumPath
		
		# put album in cache
		AlbumStore.__store[albumPath] = album

		return album
		
	#
	# Get parent album of specified album
	#
	@staticmethod
	def getParentAlbum(albumPath, errorIfNotFound=True):
		parentPath = albumPathUtils.parentPathFromChildPath(albumPath)
		return AlbumStore.getAlbum(parentPath, errorIfNotFound)
	
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
			AlbumStore.saveAlbum(parentAlbum)
		else:
			print '    Derived album thumbnail values are the same, not updating.'
		
	#
	# Save album to persistent store
	#
	@staticmethod
	def saveAlbum(album):
		'''
		Save album to persistent store, updating any parent album as needed,
		such as parentAlbum.children.title.

		Parameters
		----------
		album : Album
			album object to save

		Exception
		-----------
		Raises an exception if the save fails for any reason.
		'''

		# convert object into JSON string
		albumString = toJson.toJson(album)
		
		# get full path to album's JSON file on disk
		albumFilePath = AlbumStore.__getAlbumFilePath(album.pathComponent)
		
		if Config.doWriteToDisk:
			# write to disk
			toFile.toFile(albumFilePath, albumString)
			print '    Wrote to %s' % albumFilePath
		else:
			if Config.verbose:
				print albumString
			print '    Would have written to %s' % albumFilePath
		
		# check if we need to update derived fields on parent album
		AlbumStore.__updateParent(album)
