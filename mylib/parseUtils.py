#
# Utilities for parsing HTML files
#

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
# clean up caption 
#
def clean_caption(dirtyCaption):
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
		raise Exception('contains a HTML comment')
	
	return cleanCaption
	