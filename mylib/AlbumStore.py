#
# A persistent store of Albums and Photos
#

# import third party libraries
import glob
import os
import sys
import time
import datetime

# import my own local code
from Config import Config
from Album import Album
from Photo import Photo
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
		Raises an exception if the retrieve fails for any reason.
		'''
		
		# get full path to album's JSON file on disk
		albumFilePath = AlbumStore.__getAlbumFilePath(albumPath)
		
		# if album doesn't exist on disk, return None
		if not os.path.exists(albumFilePath):
			return None
		
		# get string of JSON from disk
		jsonString = toFile.fromFile(albumFilePath)
		
		# turn into Album object
		return toJson.fromJson(jsonString)
		
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
			
