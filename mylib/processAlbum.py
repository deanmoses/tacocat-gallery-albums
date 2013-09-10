# import external libraries
import glob
import os

# import my own local code
import processAlbumIndex
import processPhoto
from myClasses import Album

#
# process an individual album
#
def processAlbum(year, albumName, albumDir):
	'''
	process an individual album
	
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
	
	album = Album()
	album.year = year
	album.name = albumName
	
	# figure out album's index file (has album title, caption, thumbs)
	albumHtmlFile = albumDir + 'index.php' # takes precedence over .htm files
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.htm'
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.html'
	if not os.path.isfile(albumHtmlFile):
		sys.exit("cannot find album index HTML at %s" % albumHtmlFile)
	#print "   index: %s" % (albumHtmlFile)
	
	albumTitle, albumCaption = processAlbumIndex.processAlbumIndex(albumHtmlFile)
	#print "   album title: %s" % (albumTitle)
	#print "   album caption: %s" % (albumCaption)
	album.title = albumTitle
	album.caption = albumCaption
	
	# figure out the HTML and image directories
	htmlDir = albumDir + 'html/'
	imageDir = albumDir + "images/"
	
	# other years both the HTML and the images are in slides/
	if not os.path.isdir(htmlDir):
		htmlDir = albumDir + "slides/"
		imageDir = htmlDir
		
	if not os.path.isdir(htmlDir):
		sys.exit("cannot find HTML dir for %s" % albumDir)
			
	if not os.path.isdir(imageDir):
		sys.exit("cannot find image dir for %s" % albumDir)

	# for each photo...
	htmlFiles = []
	htmlFiles.extend(glob.glob(htmlDir + '*.htm'))
	htmlFiles.extend(glob.glob(htmlDir + '*.html'))
	for (htmlFile) in sorted(htmlFiles):
		photo = processPhoto.processPhoto(htmlDir, imageDir, htmlFile)
		album.photos.append(photo)

	return album
