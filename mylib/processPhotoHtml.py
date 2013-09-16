# import external libraries
import sys
import codecs
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
	# looks like most html files on disk are iso-8859-1
	# and some have accented characters that fail json.dumps
	# if we don't handle the encoding properly
	with codecs.open(htmlFile, encoding='iso-8859-1') as f:
		html = f.read()
		
		# Remove Windows /r/n newlines and a few other non-printable chars
		html = parseUtils.remove_nonprinting_chars(html)
		
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
