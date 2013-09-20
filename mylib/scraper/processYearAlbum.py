# import external libraries
import os
import sys
import time
import datetime

# import my own local code
from album.YearAlbum import YearAlbum
from store.AlbumStore import AlbumStore
from Config import Config

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

	#
	# Remove old style album paths of '12/31' -- they are duplicates
	#
	removedOldFormatAlbums = 0
	for childAlbumPath in album.children.keys():
		if not '-' in childAlbumPath:
			removedOldFormatAlbums += 1
			album.delChildAlbumThumbnail(childAlbumPath)
			print '    %s: removing duplicate thumb %s' % (year, childAlbumPath)
			
	#if removedOldFormatAlbums:
	#	print 'removed %s old albums' % removedOldFormatAlbums
	#	AlbumStore.saveAlbum(album)
	#else:
	#	print '    %s: album already exists, not re-saving' % year
	
	#
	# Update the sidebar HTML blob
	#
	sidebarFile = '%s%s.inc' % (Config.sidebarDir, year)
	with open(sidebarFile) as f:
		sidebarHtml = f.read()
		print '   firsts: %s' % (sidebarHtml)
		album.sidebar = sidebarHtml
		AlbumStore.saveAlbum(album)
		

	sys.exit()