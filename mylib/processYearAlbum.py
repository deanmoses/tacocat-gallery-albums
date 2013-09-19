# import external libraries
import os
import sys
import time
import datetime

# import my own local code
from YearAlbum import YearAlbum
from AlbumStore import AlbumStore

#
# Process a Year album, updating or creating an Album object
#
def processYearAlbum(year):
	'''
	Process a Year album, updating or creating an Album object
	
	Parameters
	----------
	year
		like 2001
				
	'''
	
	print "--------------------------\n%s: processing..." % (year)
	
	# attempt to retrieve previously created Album 
	album = AlbumStore.getAlbum(year)
	if not album:
		print '    %s: no album found, creating' % year
		album = YearAlbum()
		album.title = year
		album.pathComponent = year
		# set timestamp to Jan 1 of the year
		album.creationTimestamp = int(time.mktime(datetime.datetime(year=int(year), month=1, day=1).timetuple()))
		# save album
		AlbumStore.saveAlbum(album)
	# if already created, just validate that it has all the right stuff
	else:	
		if not album.title: raise Exception('no year %s album.title' % year)
		if not album.pathComponent: raise Exception('no year %s album.pathComponent' % year)
		if not album.creationTimestamp: raise Exception('no year %s album.creationTimestamp' % year)
		print '    %s: album already exists, not re-saving' % year

