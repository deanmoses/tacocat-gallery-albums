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
import toFile
import toJson 


#
# Ensure we have a valid album path
#
def validateAlbumPath(albumPath):
	# first 4 characters must be digits
	int(albumPath[0:4])

#
# Full path to album JSON file
#
def getAlbumFilePath(albumPath):
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
	validateAlbumPath(albumPath)
	return '%s%s/album.json' % (Config.outDir, albumPath)
	
#
# Retrieve album from persistent store
#
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
	albumFilePath = getAlbumFilePath(albumPath)
	
	# get string of JSON from disk
	jsonString = toFile.fromFile(albumFilePath)
	
	# turn into Album object
	return toJson.fromJson(jsonString)
	
#
# Save album to persistent store
#
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
	albumFilePath = getAlbumFilePath(album.pathComponent)
	
	if Config.doWriteToDisk:
		# write to disk
		toFile.toFile(albumFilePath, albumString)
		print "Wrote to %s" % albumFilePath
	else:
		if Config.verbose:
			print albumString
		print 'would have written to %s' % albumFilePath
		