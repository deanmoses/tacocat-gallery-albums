# import external libraries
import os

# import my own local code
from myClasses import Photo

#
# Process an individual photo
#
def processPhoto(htmlDir, imageDir, photoHtmlFile):
	'''
	process an individual photo
	
	Parameters
	----------
	htmlDir : string
		dir containing album's HTML files
	imageDir : string
		dir containing album's image files (may be same as htmlDir)
	photoHtmlFile : string
		full path to photo's HTML file, starting with /home/deanmoses/...
	
	Returns
	----------
	A Photo object
	'''
	photo = Photo()
	# photo name is the HTML file's name
	photoName = photoHtmlFile.replace(htmlDir, '').replace(".html", '').replace(".htm", '').strip("/")
	print "    name: %s" % (photoName)
	photo.name = photoName
	
	# get photo's image file
	imageFile = imageDir + photoName + '.JPG'
	if not os.path.isfile(imageFile):
		imageFile = imageDir + photoName + '.jpeg'
	if not os.path.isfile(imageFile):
		imageFile = imageDir + photoName + '.jpg'
	
	if not os.path.isfile(imageFile):
		sys.exit("cannot find image file for %s at %s" % (photoTitle, imageFile));
	
	photo.imageFile = imageFile
	
	return photo
