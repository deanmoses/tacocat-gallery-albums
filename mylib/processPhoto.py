# import external libraries
import os
import string
import re

# import my own local code
from Photo import Photo
import processPhotoHtml

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
	#
	# photo name is the HTML file's name
	#
	photoName = photoHtmlFile.replace(htmlDir, '').replace(".html", '').replace(".htm", '').strip("/")
	
	#
	# imageFile: path to photo's jpg
	#
	imageFile = imageDir + photoName + '.JPG'
	if not os.path.isfile(imageFile):
		imageFile = imageDir + photoName + '.jpeg'
	if not os.path.isfile(imageFile):
		imageFile = imageDir + photoName + '.jpg'
	
	if not os.path.isfile(imageFile):
		sys.exit("cannot find image file for %s at %s" % (photoTitle, imageFile));
	
	photo = Photo()
	photo.pathComponent = os.path.basename(imageFile)
	
	#
	# photo's title and caption from HTML file
	#
	photo.title, photo.description = processPhotoHtml.processPhotoHtml(photoHtmlFile)
	
	#
	# if the photo didn't have a title, use the filename 
	# but make it pretty
	#
	if not photo.title:
		# replace dashes and underscores with spaces
		# do title capitalization
		photo.title = string.capwords(photoName.replace('_', ' ').replace('-', ' '))
		
		# turn Christmas Supper1 into Christmas Supper 1
		photo.title = re.sub(r'(\d+)$', r' \1', photo.title)
		
		# turn Felixs into Felix's
		names = ['Dean', 'Lucie', 'Felix', 'Milo', 'Nana', 'Austin', 'Mike']
		for name in names:
			expression1 = name + 's '
			expression2 = name + "'s "
			photo.title = re.sub(str(expression1), str(expression2), photo.title)
		
		#print "temp title: %s" % photo.title
			
	return photo
