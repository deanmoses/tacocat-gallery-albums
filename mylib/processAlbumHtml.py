# import external libraries
import sys
from bs4 import BeautifulSoup, Comment # BeautifulSoup HTML parsing module I installed locally

# import my own local code
import processAlbumCaption

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
	with open(htmlFile) as f:
		html = f.read()
		
		# create parsed version of HTML file
		parsedHtml = BeautifulSoup(html)
		
		#
		# get title
		#
		title = parsedHtml.title.string
		
		#
		# get caption
		#
		try:
			caption = processAlbumCaption.processAlbumCaption(htmlFile, html, parsedHtml)
		except Exception as e:
			sys.exit("""\n\n
			!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			photo caption error: %s 
			%s
			http://tacocat.com/%s
			\n\n
			%s
			!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			""" % (e.message, htmlFile, htmlFile.replace('/home/deanmoses/themosii.com/', ''), html))
		
		return title, caption
