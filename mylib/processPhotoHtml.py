# import external libraries
import sys
from bs4 import BeautifulSoup, Comment # BeautifulSoup HTML parsing module I installed locally

# import my own local code
import processPhotoCaption
import parseUtils
from Config import Config
from ParseError import ParseError

#
# process photo HTML file, return title and caption
#
def processPhotoHtml(htmlFile):
	"""
	Process photo HTML file, return title and caption
	
	Parameters
	----------
	htmlFile : string
		full path to the photo's HTML file (could be .htm or .php or something else)
		
	Returns
	----------
	tuple of title, caption
	"""
	
	# open HTML file and parse title & caption out of it
	with open(htmlFile) as f:
		html = f.read()
		
		# create parsed version of HTML file
		parsedHtml = BeautifulSoup(html)
		
		#
		# get title
		#
		photoTitle = parsedHtml.title.string
		
		#
		# get caption
		#
		caption = processPhotoCaption.processPhotoCaption(htmlFile, html, parsedHtml)

		return photoTitle, caption
