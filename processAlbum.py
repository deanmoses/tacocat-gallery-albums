import processAlbumIndex

#
# process an individual album
#

def processAlbum(year, albumName, albumDir):
	
	# skip badly formatted albums, do these by hand
	badAlbumNames = ['07-ultrasound', 
		'09-bellytutu', 
		'10-doughboy', 
		'10-mermaid', 
		'12-ultrasound_bastille'] 
	if albumName in badAlbumNames: return
	badAlbumDirs = [
		'/home/deanmoses/themosii.com/pix/2004/04/08/', 
		'/home/deanmoses/themosii.com/pix/2005/12/01/',
		'/home/deanmoses/themosii.com/pix/2005/12/22/']
	if albumDir in badAlbumDirs: return
	
	print "album %s %s" % (year, albumName)
	
	album = Album()
	album.year = year
	album.name = albumName
	
	# figure out album's index HTML file that has album caption and thumbs
	albumHtmlFile = albumDir + 'index.php' # takes precedence over .htm files
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.htm'
	if not os.path.isfile(albumHtmlFile):
		albumHtmlFile = albumDir + 'index.html'
	if not os.path.isfile(albumHtmlFile):
		sys.exit("cannot find album index HTML at %s" % albumHtmlFile)
	#print "   index: %s" % (albumHtmlFile)
	
	albumTitle, albumCaption = processAlbumIndex(albumHtmlFile)
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
		photo = Photo()
		# photo name is the HTML file's name
		photoName = htmlFile.replace(htmlDir, '').replace(".html", '').replace(".htm", '').strip("/")
		#print "    name: %s" % (photoName)
		photo.name = photoName
		
		# get photo's image file
		imageFile = imageDir + photoName + '.JPG'
		if not os.path.isfile(imageFile):
			imageFile = imageDir + photoName + '.jpeg'
		if not os.path.isfile(imageFile):
			imageFile = imageDir + photoName + '.jpg'
			
		if not os.path.isfile(imageFile):
			sys.exit("cannot find image file for %s at %s" % (photoTitle, imageFile));