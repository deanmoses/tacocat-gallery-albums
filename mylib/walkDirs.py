# import third party libraries
import glob
import os
import sys
import time
import datetime

# import my own local code
import processAlbum
import processYearAlbum
from Config import Config

#
# Walk the year directory tree and process them in chronological order
# (early years first)
#
def walkDirs(albumFilter, update=False):
	'''
	Walk the directory specified by baseDir and process the albums
	
	Parameters
	----------
	albumFilter : string
		will only process the specified album(s), like:
		'2001/12/31' to process just the Dec 31, 2001 album
		'2001/12' to process all albums in Dec 2001
		'2001' to process all albums in 2001
	
	Returns
	----------
	A list of Album objects
	'''
	
	print """\n\n\n\n\n\n
------------------------------------------
----------- scraping albums --------------
------------------------------------------"""
	
	# list of albums we'll be creating
	albums = []
	
	#
	# these are all the albums I'll have to do by hand
	#

	# some year folders don't have data created by a program, do these by hand
	yearsToIgnore = ['1968ish', '1999']
	
	# skip badly formatted albums, do these by hand
	albumsToIgnore = [
		'2001/07/ultrasound', 
		'2001/09/bellytutu', 
		'2001/10/doughboy', 
		'2001/10/mermaid', 
		'2002/04/29/sasha/',
		'2002/07/21/for_austin',
		'2003/02/09/priceless',
		'2003/03/02/holly_park',
		'2003/03/09/molly_car',
		'2003/04/06/the_mint',
		'2003/12/ultrasound_bastille',
		'2003/07/27/no_links_please',
		'2004/04/08/',
		'2004/07/24/father-son/',
		'2004/08/15/audio',
		'2004/09/26/audio',
		'2005/08/window',
		'2005/11/13/evolution',
		'2005/12/01/',
		'2005/12/22/',
		'2006/newschool'
		]
		
	# return true if album is one to ignore
	def isAlbumToIgnore(albumDir):
		for albumToIgnore in albumsToIgnore:
			if albumToIgnore in albumDir: 
				return True
	
	# return true if directory is one of the normal working dirs
	normalDirs = ['slides', 'images', 'img', 'html', 'thumbnails', 'thumbs', 'res', 'video', 'audio']
	def isNormalDir(dir):
		for normalDir in normalDirs:
			if normalDir in dir:
				return True
	
	#
	# walk the year directories
	#
	for yearDir in sorted(glob.glob(Config.pixDir + '[0-9]*/')):
		year = yearDir.replace(Config.pixDir, '').strip("/")
		albumsForYear = []

		# skip all year dirs except the desired one
		if albumFilter and not albumFilter.startswith(year): 
			print "%s: skipping, it's not in %s" % (year, albumFilter)
			continue
		
		# skip all yearsToIgnore
		if year in yearsToIgnore: 
			print "%s: skipping, it's a badly formatted year" % (year)
			continue
				
		#
		# walk the month folders under the year folder
		#
		for monthDir in sorted(glob.glob(yearDir + '*/')):
			# skip all albums to ignore
			if isAlbumToIgnore(monthDir):
				print "   skipping: %s: it's a badly formatted album" % (monthDir)
				continue
				
			# if albumFilter is more than a year, use it to filter the day albums
			dayFilter = None
			if len(albumFilter) > 4:
				dayFilter = albumFilter
				
			#
			# some years are weird and have a few albums directly under them
			# mixed in with the months.  do we need to process or remove those?
			#
			if os.path.isdir(monthDir + 'slides') or os.path.isdir(monthDir + 'html'):
				raise Exception("%s: weird folder structure:  expecting month, was not one" % monthDir)

			#
			# walk the day folders under the month folder (these are individual albums)
			#
			for dayDir in sorted(glob.glob(monthDir + '*/')):
				# get album's folder path, like "2001/12/31"
				yyyyMMdd = dayDir.replace(Config.pixDir, '').strip("/")
				
				# skip all albums to ignore
				if isAlbumToIgnore(dayDir):
					print "   skipping %s: badly formatted album" % (yyyyMMdd)
					continue
				
				# skip all month dirs except the desired one
				if dayFilter and yyyyMMdd not in dayFilter: 
					print "   skipping %s: it's not in %s" % (yyyyMMdd, dayFilter)
					continue
				
				# album's created date is determined from the folder path, like "2001/12/31"
				timestamp = int(time.mktime(datetime.datetime.strptime(yyyyMMdd, "%Y/%m/%d").timetuple()))
				
				# create album
				albumsForYear.append(processAlbum.processAlbum(dayDir, timestamp, update))
				
				#
				# some albums have sub albums
				#
				for (subalbumDir) in sorted(glob.glob(dayDir + '*/')):
					if (isNormalDir(subalbumDir)): continue
					if isAlbumToIgnore(subalbumDir):
						print "   skipping: %s: it's a badly formatted album" % (subalbumDir)
						continue
						
					# create sub album
					# give it same creation date as parent album
					albumsForYear.append(processAlbum.processAlbum(subalbumDir, timestamp, update))
		
		# create year album and add it to master album list
		# but only if we're processing a full year
		if (not albumFilter) or (len(albumFilter) == 4):
			albums.append(processYearAlbum.processYearAlbum(year, albumsForYear, update))
		
		# add all the year's albums into the master album list
		albums.extend(albumsForYear)
				
	# return the album objects -- still in memory, haven't been written to disk
	return albums;
