# import external libraries
import os
import string
import re

# import my own local code
from Config import Config
from album.Photo import Photo
from album.Image import Image
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
	
	photo = Photo({})
	photo.pathComponent = os.path.basename(imageFile)
	photo.fullSizeImage = Image({})
	photo.fullSizeImage.url = Config.httpRoot + imageFile.replace(Config.webRoot, '')
	
	#
	# photo's title and caption from HTML file
	#
	photo.title, photo.description = processPhotoHtml.processPhotoHtml(photoHtmlFile)
	
	#
	# if the photo didn't have a title, use the filename 
	# but make it pretty
	#
	if not photo.title:
		# remove numbers from the start of the title,
		# they seem to always be used to order a set of photos
		# turn 10sea-horses into sea-horses
		# turn 01-julie into -julie
		photo.title = re.sub(r'^(\d+)', r'', photoName)
		
		# replace dashes and underscores with spaces
		photo.title = photo.title.replace('_', ' ').replace('-', ' ').strip()
		
		# do title capitalization
		photo.title = string.capwords(photo.title)
		
		# humanize numbers at the end of the title
		# turn Christmas Supper01 into Christmas Supper 1
		# turn Track 0 into Track
		def processEndNumber(match):
			match = match.group()
			num = int(match)
			if num == 0:
				return ''
			else:
				return ' %s' % int(match)
		
		#photo.title = re.sub(r'(\d+)$', r' \1', photo.title)
		photo.title = re.sub(r'(\d+)$', processEndNumber, photo.title)
		
		# turn Felixs into Felix's
		names = ['Dean', 'Lucie', 'Felix', 'Milo', 'Nana', 'Austin', 'Mike']
		for name in names:
			expression1 = name + 's '
			expression2 = name + "'s "
			photo.title = re.sub(str(expression1), str(expression2), photo.title)
		
		# get rid of two spaces in a row
		photo.title = photo.title.replace('  ', ' ')
		
		# sanity check that all front and rear space is gone
		photo.title = photo.title.strip()
			
	return photo
