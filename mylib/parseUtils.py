#
# Utilities for parsing HTML files
#

from ParseError import ParseError

#
# find string between two other strings
#
def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""

#
# find string between two other strings,
# starting with the rightmost occurence
# of the second string
#
def find_between_r( s, beforeString, afterString ):
	try:
		end = s.rindex( afterString )
		start = s.rindex( beforeString, 0, end) + len( beforeString )
		return s[start:end]
	except ValueError:
		return ""
	
#
# clean up caption 
#
def clean_caption(dirtyCaption, htmlFile, html, parsedHtml):
	'''
	Clean up caption (like trim it) and also
	throw exception if it contains stuff that 
	shouldn't be in there, like a <-- comment
	or a <table> tag
	
	Parameters
	----------
	dirtyCaption : string
	   caption in need of cleaning
	
	Returns
	----------
	A clean caption
	
	Throws
	----------
	Exception if caption is invalid
	'''
	
	if not dirtyCaption: return ''
	
	cleanCaption = dirtyCaption.strip()
	
	if '<!--' in cleanCaption or '-->' in cleanCaption:
		raise ParseError('caption contains a HTML comment: %s' % cleanCaption, htmlFile, html, parsedHtml)

	return cleanCaption
	