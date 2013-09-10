# import third party libraries
import glob
import os

# import my own local code
import processAlbum

#
# Walk the year directory tree and process them in chronological order
# (early years first)
#
def walkDirs(baseDir, desiredSubDirs):
	'''
	Walk the directory specified by baseDir and process the albums
	
	Parameters
	----------
	baseDir : string
	   full path to pix directory, starting with /home/deanmoses/...
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
	
	#
	# walk the year directories
	#
	for yearDir in sorted(glob.glob(baseDir + '[0-9]*/')):
		year = yearDir.replace(baseDir, '').strip("/")

		# skip all dirs except the desired one
		if desiredSubDirs and year not in desiredSubDirs: 
			print "%s: skipping, it's not in %s" % (year, desiredSubDirs)
			continue
		
		# skip all yearsToIgnore
		if year in yearsToIgnore: 
			print "%s: skipping, it's a badly formatted year" % (year)
			continue
		
		#print '%s' % (year)
		
		#
		# walk the month directories
		#
		for monthDir in sorted(glob.glob(yearDir + '*/')):
			month = monthDir.replace(yearDir, '').strip("/")
			#print "%s/%s" % (year, month)
			
			#
			# some years are weird and have a few albums directly under them
			# detect those here and process them
			#
			if os.path.isdir(monthDir + 'slides') or os.path.isdir(monthDir + 'html'):
				albumName = month
				albums.append(processAlbum.processAlbum(year, albumName, monthDir))
				continue
			
			#
			# walk the days under the months (these are individual albums)
			#
			for dayDir in sorted(glob.glob(monthDir + '*/')):
				day = dayDir.replace(monthDir, '').strip("/")
				albumName = "%s-%s" % (month, day)
				
				# skip all albumsToIgnore
				if isAlbumToIgnore(dayDir):
					print "   skipping: %s %s: it's a badly formatted album" % (year, albumName)
					continue

				albums.append(processAlbum.processAlbum(year, albumName, dayDir))
	
	# return the album objects -- still in memory, haven't been written to disk
	return albums;
