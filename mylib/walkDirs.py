# import third party libraries
import glob
import os
import sys

# import my own local code
import processAlbum
import processYearAlbum
from Config import Config

#
# Walk the year directory tree and process them in chronological order
# (early years first)
#
def walkDirs(desiredSubDirs):
	'''
	Walk the directory specified by baseDir and process the albums
	
	Parameters
	----------
	desiredSubDirs : [] of strings
		only process these dirs, like ['1969']
	
	Returns
	----------
	A list of Album objects
	'''
	
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
		'2003/12/ultrasound_bastille'
		'2004/04/08/', 
		'2005/12/01/',
		'2005/12/22/']
		
	# return true if album is one to ignore
	def isAlbumToIgnore(albumDir):
		for albumToIgnore in albumsToIgnore:
			if albumToIgnore in albumDir: 
				return True
	
	# return true if directory is one of the normal working dirs
	normalDirs = ['slides', 'images', 'html', 'thumbnails', 'res', 'video']
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

		# skip all dirs except the desired one
		if desiredSubDirs and year not in desiredSubDirs: 
			print "%s: skipping, it's not in %s" % (year, desiredSubDirs)
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
			
			#
			# some years are weird and have a few albums directly under them
			# mixed in with the months.  do we need to process or remove those?
			#
			if os.path.isdir(monthDir + 'slides') or os.path.isdir(monthDir + 'html'):
				raise Exception("weird folder structure:  expecting month, was not one")
				albumsForYear.append(processAlbum.processAlbum(monthDir))
				continue
			
			#
			# walk the day folders under the month folder (these are individual albums)
			#
			for dayDir in sorted(glob.glob(monthDir + '*/')):
				# skip all albums to ignore
				if isAlbumToIgnore(dayDir):
					print "   skipping: %s: it's a badly formatted album" % (dayDir)
					continue
								
				albumsForYear.append(processAlbum.processAlbum(dayDir))
				
				#
				# some albums have sub albums
				#
				for (subalbumDir) in sorted(glob.glob(dayDir + '*/')):
					if (isNormalDir(subalbumDir)): continue
					if isAlbumToIgnore(subalbumDir):
						print "   skipping: %s: it's a badly formatted album" % (subalbumDir)
						continue
					albumsForYear.append(processAlbum.processAlbum(subalbumDir))
		
		# create year album and add it to master album list
		albums.append(processYearAlbum.processYearAlbum(year, albumsForYear))
		
		# add all the year's albums into the master album list
		albums.extend(albumsForYear)
				
	# return the album objects -- still in memory, haven't been written to disk
	return albums;
