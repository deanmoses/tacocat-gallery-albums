#
# process album's index HTML file
#

# import external libraries
import sys
from bs4 import BeautifulSoup, Comment # BeautifulSoup HTML parsing module I installed locally
import codecs

# import my own local code
import parseUtils
import processAlbumCaption
from ParseError import ParseError

#
# process album index HTML file, return title and caption
# return tuple of title, caption
#
def processAlbumHtml(htmlFile):
	"""
	Process album index HTML file, return title and caption
	
	Parameters
	----------
	indexHtmlFile : string
		full path to the album's index HTML file (could be .htm or .php or something else)
		
	Returns
	----------
	tuple of title, caption
	"""
	
	# open album index file and parse title & caption out of it
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
		title = parsedHtml.title.string
		
		if title:
			# we don't want album titles like "January 1, 2002"
			stopwords = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
			for stopword in stopwords:
				if stopword in title.lower():
					title = ''
				
		#
		# get caption
		#
		try:
			caption = processAlbumCaption.processAlbumCaption(htmlFile, html, parsedHtml)
		except AssertionError as e:
			url = htmlFile.replace('/home/deanmoses/themosii.com/', '')
			sys.exit("""\n\n
			!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			photo caption error: %s 
			%s
			http://tacocat.com/%s
			\n\n
			%s
			!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			""" % (e.message, htmlFile, url, html))
		
		return title, caption
