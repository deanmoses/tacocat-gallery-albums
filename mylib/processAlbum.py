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
def processAlbum(albumDir, creationTimestamp, update=True):
	'''
	Process an individual album, creating an Album object.
	This is for week albums and subalbums.  *NOT* for year albums.
	
	Parameters
	----------
	albumDir : string
		full path to album, like /home/deanmoses/...
		
	update : boolean
		false: replace the contents of the existing Album
		true: do an incremental update, just replacing a few new things
	
	Returns
	----------
	An Album object
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

	# if not found, create Album
	if not album:
		print '    %s: no album found, creating.' % pathComponent
		album = Album()

	if update:
		if not album.pathComponent: raise Exception('no album.pathComponent in %s' % pathComponent)
		if not album.creationTimestamp: raise Exception('no album.creationTimestamp in %s' % pathComponent)
		if not album.title: raise Exception('no album.title')
	else:	
		album.pathComponent = pathComponent
		
		# album's created date
		album.creationTimestamp = creationTimestamp
		
		# album's title is the long format day, like "December 1".  No year.
		album.title = datetime.datetime.fromtimestamp(album.creationTimestamp).strftime('%B %-d')

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
		# extract summary and caption from album's HTML file
		#
		if update:			
			# too many albums don't have summaries to do this sanity check
			#if not album.summary: raise Exception('no album.summary in %s' % pathComponent)
			
			# too many albums don't have descriptions to do this sanity check
			#if not album.description: raise Exception('no album.description')
			pass
		else:
			album.summary = processAlbumHtml.scrapeSummary(parsedHtml)
			
			album.description = processAlbumHtml.scrapeCaption(albumHtmlFile, html, parsedHtml)
			if (Config.verbose): print "    Caption: %s" % album.description
			
			album.childrenOrder = processAlbumHtml.scrapePhotoOrder(albumHtmlFile, html, parsedHtml)
			if len(album.childrenOrder) < 3:
				sys.exit('    Got less than %s thumbs for album %s: %s' % (3, albumHtmlFile, album.childrenOrder))
			print "    children order: %s" % album.childrenOrder
	
	#
	# Process photos
	#
	
	# the old children format was a list, moved to a dict
	# once I run through all albums once I could remove this
	if isinstance(album.children, list):
		print '    album %s children were old format (list), converting to dict' % pathComponent
	album.children = {}
	
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
		sys.exit("    cannot find HTML dir for %s" % albumDir)
		
	if not os.path.isdir(imageDir):
		sys.exit("    cannot find image dir for %s" % albumDir)

	#
	# process each photo
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
		
	# save album
	AlbumStore.saveAlbum(album)
		
	return album
