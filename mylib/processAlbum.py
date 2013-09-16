# import external libraries
import glob
import os
import sys
import textwrap
import time
import datetime

# import my own local code
import processAlbumHtml
import processPhoto
import parseUtils
from Album import Album
from Config import Config

#
# Process an individual album, creating an Album object
#
def processAlbum(albumDir, creationTimestamp):
	'''
	Process an individual album, creating an Album object
	
	Parameters
	----------
	albumDir : string
		full path to album, like /home/deanmoses/...
	
	Returns
	----------
	An Album object
	'''
	
	# create the Album we'll be returning
	album = Album()
	
	# path, like "2001/12/31" for normal week albums
	# or "2001/12/31/schoolpix" for sub albums
	album.pathComponent = albumDir.replace(Config.pixDir, '').strip("/")
	
	# album's created date
	album.creationTimestamp = creationTimestamp
	
	# it's a sub album if the path has more than 2 slashes
	# 2001/12/31" vs "2001/12/31/schoolpix"
	isSubAlbum = album.pathComponent.count('/') > 2
	
	# album's title is the long format day, like "December 31".  No year.
	album.title = datetime.datetime.fromtimestamp(album.creationTimestamp).strftime('%B %d')

	print "   %s" % (album.pathComponent)
	
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
	
	album.summary, album.description = processAlbumHtml.processAlbumHtml(albumHtmlFile)
		
	if (Config.verbose): print "caption: %s" % album.description
		
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
		album.children.append(photo)

		if Config.verbose:
			print "    %s" % (photo.pathComponent)
			
		if (Config.verbose and photo.description): 
			w = textwrap.TextWrapper(width=70,break_long_words=False,replace_whitespace=False,initial_indent='      ',subsequent_indent='      ')
			print w.fill(photo.description)
			#print "      %s" % (photo.description)
			

	return album
