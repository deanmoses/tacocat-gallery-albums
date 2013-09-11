#
# Configuration of the script - exposes paths and such
#
class Config:
	
	# root of tacocat webserver
	webRoot = '/home/deanmoses/themosii.com/'

	# root of tacocat static HTML albums
	pixDir = webRoot + 'pix/' 

	# root of this script
	scriptDir = '/home/deanmoses/scrape/'

	# dir to write output to
	outDir = scriptDir + 'output/'  

	# file with paths of photos that don't have captions
	noCaptionsFile = scriptDir + 'photosWithoutCaptions.txt' 
	
	# output verbose logging
	# this is set by a command line option
	verbose = False
