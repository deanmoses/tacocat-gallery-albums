# import external libraries
import sys
from bs4 import BeautifulSoup, Comment # BeautifulSoup HTML parsing module I installed locally

#
# process album index file, return caption
# return tuple of title, caption
#
def processAlbumIndex(indexHtmlFile):	
	# open album index file and parse title & caption out of it
	with open(indexHtmlFile) as f:
		html = f.read()
		
		parsedHtml = BeautifulSoup(html)
		albumTitle = parsedHtml.title.string
		#print 'album title: %s' % (albumTitle)
		
		#
		# some albums genuinely don't have captions
		#
		noCaptions = ['2001/12', '2002/01', '2002/02', '2002/03/04', '2002/03/11', '2002/03/18']
		for noCaption in noCaptions:
			if noCaption in indexHtmlFile: 
				return albumTitle, ''
		
		def find_between( s, first, last ):
		    try:
		        start = s.index( first ) + len( first )
		        end = s.index( last, start )
		        return s[start:end]
		    except ValueError:
		        return ""
		
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
		
		sys.exit("cannot find album caption %s" % parsedHtml)
