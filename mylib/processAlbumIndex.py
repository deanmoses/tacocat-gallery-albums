# import external libraries
import sys
from bs4 import BeautifulSoup, Comment # BeautifulSoup HTML parsing module I installed locally

# import my own local code
from parseUtils import find_between

#
# process album index HTML file, return title and caption
# return tuple of title, caption
#
def processAlbumIndex(indexHtmlFile):
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
	with open(indexHtmlFile) as f:
		html = f.read()
		
		parsedHtml = BeautifulSoup(html)
		albumTitle = parsedHtml.title.string
		#print 'album title: %s' % (albumTitle)
		
		#
		# some albums genuinely don't have captions
		#
		noCaptions = [
			'2001/12', # none of the 5 albums in december 2001 have captions
			'2002/01', 
			'2002/02', 
			'2002/03/04', 
			'2002/03/11', 
			'2002/03/18']
		for noCaption in noCaptions:
			if noCaption in indexHtmlFile: 
				return albumTitle, ''
		
		# some very early albums
		caption = find_between(html, '<!-- Include header.inc from image directory if present -->', '<!-- Iterate through images and produce an index table -->')
		if caption:
			caption = caption.replace('<br>&nbsp;<br>', '').strip()
			return albumTitle, caption
			
		caption = find_between(html, '<div bgcolor="#bde6d8" style="width:600px">', '</div>')
		if caption:
			caption = caption.strip()
			return albumTitle, caption
			
		caption = find_between(html, '</TABLE>', 'Return to <a href="http://www.tacocat.com/felix/">main Felix page</a>.')
		if caption:
			caption = caption.strip()
			return albumTitle, caption
			
		caption = find_between(html, 
			'</TABLE>', 
			'<TABLE border="0" cellpadding="0" cellspacing="10" bgcolor="#FFFFFF" >')
		if caption:
			caption = caption.strip()
			return albumTitle, caption			
		
		if not parsedHtml.body:
			sys.exit("cannot find parsedHtml.body %s" % parsedHtml) 
		
		caption = parsedHtml.body.find('p', attrs={'class':'para'})
		
		if caption:
			return albumTitle, caption
		
		sys.exit("cannot find caption for album %s\n%s" % (indexHtmlFile, parsedHtml))
