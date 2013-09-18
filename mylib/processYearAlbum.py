# import external libraries
import glob
import os
import sys
import textwrap
import time
import datetime
import copy

# import my own local code
from Album import Album
from Image import Image
from Config import Config
from AlbumStore import AlbumStore

#
# Process a Year album, creating an Album object
#
def processYearAlbum(year, subalbums, update=True):
	'''
	Process a Year album, creating an Album object
	
	Parameters
	----------
	year
		like 2001
		
	subalbums : [Album]
		list of my child albums, each one representing a week
		
	Returns
	----------
	An Album object for the overall year
	'''
	
	print "  %s" % (year)
	
	# retrieve the Album we'll be updating
	album = AlbumStore.getAlbum(year)
	
	if update:
		if not album.title: raise Exception('no year %s album.title' % year)
		if not album.pathComponent: raise Exception('no year %s album.pathComponent' % year)
		if not album.creationTimestamp: raise Exception('no year %s album.creationTimestamp' % year)
	else:
		album.title = year
		album.pathComponent = year
	
		# set timestamp to Jan 1 of the year
		album.creationTimestamp = int(time.mktime(datetime.datetime(year=int(year), month=1, day=1).timetuple()))

	if isinstance(album.children, list):
		print 'year %s subalbums were old format (list), converting to dict' % year
		album.children = {}
			
	# add just enough info about each child album to let the
	# client generate thumbnails w/o having to retrieve the
	# subalbums
	for subalbum in subalbums:
		# clone the child album
		smallChild = copy.copy(subalbum)
	
		# remove information not needed for thumbnails
		del(smallChild.description)
		del(smallChild.children)
		del(smallChild.childrenOrder)
	
		# randomly choose a photo from subalbum to use as its thumbnail in the year album
		# will choose a different one manually later
		randomPhoto = subalbum.children.itervalues().next()
		smallChild.fullSizeImage = Image({})
		smallChild.fullSizeImage.url = randomPhoto.fullSizeImage.url
	
		# add subalbum to my list of children
		album.children[smallChild.pathComponent] = smallChild
	
	# save album
	AlbumStore.saveAlbum(album)
	
	return album
