#
# Configuration of both the scrape script and the album store - exposes paths and such
#
class Config:
	
	# root of tacocat webserver
	webRoot = '/home/deanmoses/themosii.com/'

	# root of tacocat static HTML albums
	pixDir = webRoot + 'pix/'
	
	# root of tacocat.com
	httpRoot = 'http://tacocat.com/' 

	# root of this script
	scriptDir = '/home/deanmoses/scrape/'

	# dir to write output to
	outDir = webRoot + 'oldpix/'  

	# file with paths of photos that don't have captions
	noCaptionsFile = scriptDir + 'photosWithoutCaptions.txt' 
	
	# output verbose logging
	# this is set by a command line option
	verbose = False
	
	# save albums to disk
	# this is set by a command line option
	doWriteToDisk = True