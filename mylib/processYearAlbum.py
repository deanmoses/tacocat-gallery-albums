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

#
# Process a Year album, creating an Album object
#
def processYearAlbum(year, subalbums):
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
	
	# create the Album we'll be returning
	album = Album()
	album.title = year
	album.pathComponent = year
	
	# set timestamp to Jan 1 of the year
	album.creationTimestamp = int(time.mktime(datetime.datetime(year=int(year), month=1, day=1).timetuple()))

	print "  %s" % (album.pathComponent)
	
	# add just enough info about each child album to let the
	# client generate thumbnails w/o having to retrieve the
	# subalbums
	for subalbum in subalbums:
		# clone the child album
		smallChild = copy.copy(subalbum)
		
		# remove information not needed for thumbnails
		del(smallChild.description)
		del(smallChild.children)
		
		# randomly choose the album's first picture to use as the album's thumbnail
		# will choose a different one manually later
		smallChild.fullSizeImage = Image()
		smallChild.fullSizeImage.url = subalbum.children[0].fullSizeImage.url
		
		# add subalbum to my list of children
		album.children.append(smallChild)
	
	return album