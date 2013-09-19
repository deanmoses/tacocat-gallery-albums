# import external libraries
import glob
import os
import sys
import textwrap
import time
import datetime
from bs4 import BeautifulSoup, Comment # BeautifulSoup HTML parsing module I installed locally
import codecs

# import my own local code
import processAlbumHtml
import processPhoto
import parseUtils
import albumPathUtils
from AlbumStore import AlbumStore
from Album import Album
from Config import Config

#
# Process an individual album, creating an Album object
#
def processAlbum(albumDir, creationTimestamp):
	'''
	Process an individual album, creating an Album object.
	This is for week albums and subalbums.  *NOT* for year albums.
	
	Parameters
	----------
	albumDir : string
		full path to album, like /home/deanmoses/...
	'''
	
	# figure out the pathComponent, which is the logical path used in 
	# the web UI, like "2001/12-31" for normal week albums
	# or "2001/12-31/schoolpix" for sub albums
	albumShortPath = albumDir.replace(Config.pixDir, '').strip("/")
	pathComponent = albumPathUtils.albumPathFromDiskPath(albumShortPath)
	
	# it's a sub album if the path has more than 2 slashes
	# 2001/12-31" vs "2001/12-31/schoolpix"
	isSubAlbum = pathComponent.count('/') > 1
	
	print "--------------------------\n%s: processing..." % (pathComponent)

	# retrieve the Album we'll be updating
	album = AlbumStore.getAlbum(pathComponent)
	isNew = not album
	
	# if not found, create Album
	if isNew:
		album = Album()
		album.pathComponent = pathComponent
		
		# album's created date
		album.creationTimestamp = creationTimestamp
		
		# album's title is the long format day, like "December 1".  No year.
		album.title = datetime.datetime.fromtimestamp(album.creationTimestamp).strftime('%B %-d')
		
	# otherwise just validate the existing data
	else:
		if not album.pathComponent: raise Exception('no album.pathComponent in %s' % pathComponent)
		if not album.creationTimestamp: raise Exception('no album.creationTimestamp in %s' % pathComponent)
		if not album.title: raise Exception('no album.title')
		
		
	#
	# figure out path to album's index HTML file
	#
	albumHtmlFile = albumDir + 'index.php' # newer .php takes precedence over older .htm files
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.htm'
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.html'
	if not os.path.isfile(albumHtmlFile):
		sys.exit("cannot find album index HTML at %s" % albumHtmlFile)

	#
	# figure out path to album's HTML and image directories
	#
	htmlDir = albumDir + 'html/'
	imageDir = albumDir + "images/"
	if not os.path.isdir(htmlDir):
		htmlDir = albumDir + "slides/"
		imageDir = htmlDir
	if not os.path.isdir(htmlDir):
		sys.exit("    cannot find HTML dir for %s" % albumDir)
	if not os.path.isdir(imageDir):
		sys.exit("    cannot find image dir for %s" % albumDir)
			
	#
	# read album index file and parse stuff out of it, like the album's caption
	#
	# It looks like most HTML files on disk are iso-8859-1
	# and some have accented characters that cause json.dumps
	# to error if we don't handle the encoding properly here.
	with codecs.open(albumHtmlFile, encoding='iso-8859-1') as f:
		html = f.read()

		# Remove Windows /r/n newlines and a few other non-printable chars
		html = parseUtils.remove_nonprinting_chars(html)

		# create parsed version of HTML file
		parsedHtml = BeautifulSoup(html)
			
		#
		# extract summary, caption and child order from album's HTML file
		#
		if isNew:
			album.summary = processAlbumHtml.scrapeSummary(parsedHtml)
			
			album.description = processAlbumHtml.scrapeCaption(albumHtmlFile, html, parsedHtml)
			if (Config.verbose): print "    Caption: %s" % album.description
			
			album.childrenOrder = processAlbumHtml.scrapePhotoOrder(albumHtmlFile, html, parsedHtml)
			if len(album.childrenOrder) < 2:
				sys.exit('    Got less than %s thumbs for album %s: %s' % (2, albumHtmlFile, album.childrenOrder))
			print "    children order: %s" % album.childrenOrder
	
	#
	# Process photos
	#
	
	htmlFiles = []
	htmlFiles.extend(glob.glob(htmlDir + '*.htm'))
	htmlFiles.extend(glob.glob(htmlDir + '*.html'))
	for (htmlFile) in sorted(htmlFiles):
		
		# from some/path/to/supper.jpg, get supper
		photoName = htmlFile.rsplit('/', 1)[1].rsplit('.', 1)[0]

		# error if there are photo HTML files that aren't in the thumbnail order
		if (photoName not in album.childrenOrder):
			print '    Photo %s is not in %s\n    childrenOrder: %s' % (photoName, album.pathComponent, album.childrenOrder)
			continue
		
		if isNew:
			photo = processPhoto.processPhoto(htmlDir, imageDir, htmlFile)
			album.children[photoName] = photo
			
			if Config.verbose:
				print "    %s: processing..." % (photo.pathComponent)
		
			if (Config.verbose and photo.description): 
				w = textwrap.TextWrapper(width=70,break_long_words=False,replace_whitespace=False,initial_indent='      ',subsequent_indent='      ')
				print w.fill(photo.description)
				#print "      %s" % (photo.description)
	
	# Verify that chidrenOrder contains all the photos
	# we just added.  If it doesn't, that means the
	# thumbnail scraping wasn't good.
	childrenNames = album.children.keys()
	for childOrderName in album.childrenOrder:
		if childOrderName not in childrenNames:
			raise Exception('Album %s: children contains photo %s, which is not in childOrder.\nchildOrder: %s\nchildren: %s' % (album.pathComponent, childOrderName, album.childOrder, album.children))
			
	if len(album.childrenOrder) != len(album.children):
		raise Exception('Album %s: childOrder length (%s) is not same same as children length (%s).\nchildOrder: %s\nchildren: %s' % (album.pathComponent, len(album.childrenOrder), len(album.children), album.childOrder, album.children))
	
	# randomly choose a photo to be the album thumbnail
	if not album.getAlbumThumbnailPhoto():
		randomPhotoName = album.children.iterkeys().next()
		album.setAlbumThumbnailPhoto(randomPhotoName)
		print '    %s: no thumbnail set, setting to %s' % (album.pathComponent, randomPhotoName)
	
	# save album
	AlbumStore.saveAlbum(album)