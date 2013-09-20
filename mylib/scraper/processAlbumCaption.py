# import external libraries
import sys

# import my own local code
import parseUtils
from ParseError import ParseError

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
	caption = parseUtils.find_between(html, '<!-- Include header.inc from image directory if present -->', '<!-- Iterate through images and produce an index table -->')
	if caption:
		caption = caption.replace('<br>&nbsp;<br>', '').strip()
		return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	#
	#
	caption = parseUtils.find_between(html, '<div bgcolor="#bde6d8" style="width:600px">', '</div>')
	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Circa 2003/12
	# <TD><H2><FONT color="#000000"> December 15-21</H2></FONT></TD>
	# </TR>
	# </TABLE>
	# <P>
	# <P>
	# Caption goes here
	# <p>
	# Return to <a href="http://tacocat.com/felix/">main Felix page</a>.
	# </p>
	caption = parseUtils.find_between_r(html, 
"""</TABLE>
<P>
<P>""", 
"""<p>
Return to <a href="http://tacocat.com/felix/">main Felix page</a>""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)	
	
	#
	#
	#
	caption = parseUtils.find_between(html, '</TABLE>', 'Return to <a href="http://www.tacocat.com/felix/">main Felix page</a>.')
	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	
	#
	# Albums circa 2003/11:
	#
	# <H2><FONT color="#000000"> October 27 - November 2</H2></FONT></TD>
	# Caption goes here
	# <p>
	# Return to <a href="http://tacocat.com/felix/">main Felix page</a>.
	# </p>
	caption = parseUtils.find_between_r(html, 
"""</H2></FONT></TD>""", 
"""<p>
Return to <a href="http://tacocat.com/felix/">main Felix page</a>""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
		
	#
	# Albums circa 2003/12/28:
	# 
	# <H2><FONT color="#000000"> December 22-28</H2></FONT>
	# Caption goes here
	# <p>
	# Return to <a href="http://tacocat.com/felix/">main Felix page</a>.
	# </p>
	#
	# -------
	# Albums circa 2004/01:
	#
	# <H2><FONT color="#000000"> January 19 - 25</H2></FONT>
	# Caption goes here
	# <p>
	# Return to <a href="../../index.html">main 2004 page</a>.
	# </p>
	caption = parseUtils.find_between_r(html, 
"""</H2></FONT>""", 
"""<p>
Return to <a href=""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Albums circa 2004/3:
	#
	# <H2><FONT color="#000000"> March 20-21</H2></FONT>
	# Caption goes here
	# <p>
	# Return to the <a href="../index.htm">rest of this week's photos</a>.
	# </p>
	caption = parseUtils.find_between_r(html, 
"""</H2></FONT>""", 
"""<p>
Return to the <a href=""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Albums circa 2004/01:
	#
	# <H2><FONT color="#000000"> December 29 - January 4</FONT></H2>
	# Caption
	# Return to <a href="../../index.html">main 2004 page</a>.
	#
	# Albums circa 2004/09:
	# <H2>September 26</H2>
	# Caption goes here
	# <p>
	# Return to <a href="../../index.html">main 2004 page</a>.
	caption = parseUtils.find_between_r(html, 
"""</H2>""", 
"""Return to <a href="../../index.html">""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)

	#
	#
	#
	caption = parseUtils.find_between(html, 
		'</TABLE>', 
		'<TABLE border="0" cellpadding="0" cellspacing="10" bgcolor="#FFFFFF" >')
	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)			
	
	#
	# Albums starting 2005/01
	#
	# <hr size=1 color="#F19753" />
	#
	# <!-- Include header.inc from the source image directory if present -->
	# Caption goes here
	# <br>&nbsp;<br>
	#
	#<!-- Table of thumbnails -->
	#
	caption = parseUtils.find_between_r(html, 
"""<!-- Include header.inc from the source image directory if present -->""", 
"""<br>&nbsp;<br>""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Albums starting 2005/04
	#
	# <!-- Include header.inc from the source image directory if present -->
	# Caption goes here
	# <!-- Table of thumbnails -->
	#
	caption = parseUtils.find_between_r(html, 
"""<!-- Include header.inc from the source image directory if present -->""", 
"""<!-- Table of thumbnails -->""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Albums starting 2006/07
	#
	# <hr size=1 color="#F19753" />
	# Caption goes here	
	# <br>&nbsp;<br>
	#
	caption = parseUtils.find_between_r(html, 
"""<hr size=1 color="#F19753" />""", 
"""<br>&nbsp;<br>""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)	

	#
	# if we haven't figured out a caption at this point, we need
	# to improve the parsing. 
	#
	if not caption: raise ParseError('no album caption found', htmlFile, html, parsedHtml)
		
	return caption
