#
# Utilities for parsing HTML files
#

# third party libs
import sys

# import my own libs
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
		#if 'Our house' in s: pdb.set_trace()
		end = s.rindex( afterString )
		#print 'end: %s' % end
		start = s.rindex( beforeString, 0, end) + len( beforeString )
		#print 'start: %s' % start
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
	
	if not dirtyCaption: 
		return ''
	
	# not sure how some captions aren't being returned as strings, but it's happening, rarely
	cleanCaption = dirtyCaption.strip()

	# check for stuff that would indicate that parsing went wrong
	disallowedThings = ['<!--', '-->', '<table', '</table>']
	for disallowedThing in disallowedThings:
		if disallowedThing in cleanCaption:
			raise ParseError('caption contains a [%s]: %s' % (disallowedThing, cleanCaption), htmlFile, html, parsedHtml)

	return cleanCaption

#
# Remove Windows /r/n newlines and a few other non-printable chars
#
def remove_nonprinting_chars(input):
	translation_table = dict.fromkeys(map(ord, '\r\v\f'), None)
	return input.translate(translation_table)
