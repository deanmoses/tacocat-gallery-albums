# import external libraries
import sys

# import my own local code
from parseUtils import find_between

#
# extract album caption from album HTML file
#
def processAlbumCaption(htmlFile, html, parsedHtml):
	"""
	Extract the album's caption from the album HTML file
	
	Parameters
	----------
	htmlFile : string
		full path to the HTML file (could be .htm or .php or other)
	
	html : string
		raw text of HTML file
		
	parsedHtml : BeautifulSoup
		BeautifulSoup object representing parsed HTML file
		
	Returns
	----------
	caption: string
	"""
	
	caption = ''
	
	#
	# some albums genuinely don't have captions
	#
	noCaptions = [
		'2001/12', # none of the 5 albums in december 2001 have captions
		'2002/01', 
		'2002/02', 
		'2002/03/04', 
		'2002/03/11', 
		'2002/03/18'
		]
		
	for noCaption in noCaptions:
		if noCaption in htmlFile: 
			return caption
	
	#####################################################
	# now try a whole bunch of different parsing routines
	#####################################################
	
	#
	# some very early albums
	#
	caption = find_between(html, '<!-- Include header.inc from image directory if present -->', '<!-- Iterate through images and produce an index table -->')
	if caption:
		caption = caption.replace('<br>&nbsp;<br>', '').strip()
		return caption
	
	#
	#
	#
	caption = find_between(html, '<div bgcolor="#bde6d8" style="width:600px">', '</div>')
	if caption:
		caption = caption.strip()
		return caption
	
	#
	#
	#
	caption = find_between(html, '</TABLE>', 'Return to <a href="http://www.tacocat.com/felix/">main Felix page</a>.')
	if caption:
		caption = caption.strip()
		return caption
	
	#
	#
	#
	caption = find_between(html, 
		'</TABLE>', 
		'<TABLE border="0" cellpadding="0" cellspacing="10" bgcolor="#FFFFFF" >')
	if caption:
		caption = caption.strip()
		return caption			
	
	
	#
	#
	#
	if not parsedHtml.body:
		sys.exit("cannot find parsedHtml.body %s" % parsedHtml) 
	
	caption = parsedHtml.body.find('p', attrs={'class':'para'})
	
	if caption: return caption
	

	
	#
	# if we haven't figured out a caption at this point, we need
	# to improve the parsing.  print out some diagnostics and exit
	#
	
	if not caption:
		sys.exit("""\n\n
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cannot find caption for album 
%s
http://tacocat.com/%s
\n\n
%s
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""" % (htmlFile, htmlFile.replace('/home/deanmoses/themosii.com/', ''), html))
		
	return caption
