# import external libraries
import glob
import os
import sys
import textwrap

# import my own local code
import processAlbumHtml
import processPhoto
import parseUtils
from myClasses import Album
from config import Config

#
# Process an individual album, creating an Album object
#
def processAlbum(year, albumName, albumDir):
	'''
	Process an individual album, creating an Album object
	
	Parameters
	----------
	year : string
	   like '2005'
	albumName : string
		like '12-31'
	albumDir : string
		full path to album, like /home/deanmoses/...
	
	Returns
	----------
	An Album object
	'''
	
	print "  %s/%s" % (year, albumName)
	
	# create the Album we'll be returning
	album = Album()
	album.year = year
	album.name = albumName
	
	#
	# figure out path to album's index HTML file (has album title and caption)
	#
	
	albumHtmlFile = albumDir + 'index.php' # newer .php takes precedence over older .htm files
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.htm'
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.html'
	if not os.path.isfile(albumHtmlFile):
		sys.exit("cannot find album index HTML at %s" % albumHtmlFile)
	
	#
	# extract title and caption from album's HTML file
	#
	
	album.title, album.caption = processAlbumHtml.processAlbumHtml(albumHtmlFile)
		
	if (Config.verbose): print "caption: %s" % album.caption
		
	#
	# figure out path to album's HTML and image directories
	#
	
	htmlDir = albumDir + 'html/'
	imageDir = albumDir + "images/"
	
	# in other years, both the HTML and the images are in slides/
	if not os.path.isdir(htmlDir):
		htmlDir = albumDir + "slides/"
		imageDir = htmlDir
		
	if not os.path.isdir(htmlDir):
		sys.exit("cannot find HTML dir for %s" % albumDir)
			
	if not os.path.isdir(imageDir):
		sys.exit("cannot find image dir for %s" % albumDir)

	#
	# process each photo
	#
	htmlFiles = []
	htmlFiles.extend(glob.glob(htmlDir + '*.htm'))
	htmlFiles.extend(glob.glob(htmlDir + '*.html'))
	for (htmlFile) in sorted(htmlFiles):
		photo = processPhoto.processPhoto(htmlDir, imageDir, htmlFile)
		album.photos.append(photo)

		print "    %s" % (photo.name)
		if (Config.verbose and photo.caption): 
			w = textwrap.TextWrapper(width=70,break_long_words=False,replace_whitespace=False,initial_indent='      ',subsequent_indent='      ')
			print w.fill(photo.caption)
			#print "      %s" % (photo.caption)
			

	return album
