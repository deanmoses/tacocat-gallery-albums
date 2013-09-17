# import external libraries
import sys
import string

# import my own local code
import parseUtils
from Config import Config
from ParseError import ParseError

#
# process photo HTML file, return caption
#
def processPhotoCaption(htmlFile, html, parsedHtml):
	"""
	Parse caption out of parsedHtml
	
	Parameters
	----------
	htmlFile : string
		full path to the photo's HTML file (could be .htm or .php or something else)
	
	html : string
		text of HTML file
		
	parsedHtml : BeautifulSoup
		beautifulSoup object representing parsed HTML file
		
	Returns
	----------
	caption: string
	"""
	
	caption = ''
	
	#
	# Some photos genuinely don't have captions.
	# Read list of paths to ignore from text file.
	# Ignore any photos that match the paths,
	# which could be things like '2001/12/13/'
	# that exclude all photos in the album.
	#
	with open(Config.noCaptionsFile) as f:
		noCaptions = f.read().split()
		for noCaption in noCaptions:
			if not noCaption: continue # ignore blank lines in file
			if noCaption in htmlFile: 
				return caption
	
	#####################################################
	# now try a whole bunch of different parsing routines
	#####################################################
	
	#
	# Albums circa 2001:
	#
	# <!--
	# File: C:\Documents and Settings\moses.MOSESREMOTE\My Documents\My Pictures\tacocat\felix\2001.12.17-23\raw_images\maman_dans_la_cuisine.txt
	# -->
	# Caption goes here 
	# <P>
	# <CENTER>
	# <TABLE border="0" cellpadding="0" cellspacing="2" width="200" bgcolor="#FFFFFF" >
	#
	caption = parseUtils.find_between_r(html, 
"""-->""", 
"""<P>
<CENTER>
<TABLE border="0" cellpadding="0" cellspacing="2" width="200" bgcolor="#FFFFFF" >""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)

	#
	# Albums 2001-2004:
	#
	# </TABLE>
	# </CENTER>
	# <P>
	# <P>
	# Caption goes here
	# <P>
	# <CENTER>
	# <TABLE border="0" cellpadding="0" cellspacing="2" width="200" bgcolor="#FFFFFF" >
	#
	caption = parseUtils.find_between_r(html, 
"""</TABLE>
</CENTER>
<P>
<P>""", 
"""<P>
<CENTER>
<TABLE border="0" cellpadding="0" cellspacing="2" width="200" bgcolor="#FFFFFF" >""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)

	#
	# Albums starting 2005/01:
	#
	# <!-- Commentary on the picture -->
	#
	# <br>
	# Caption goes here
	# <br>&nbsp;<br>
	#
	caption = parseUtils.find_between_r(html, 
"""<!-- Commentary on the picture -->

<br>""", 
"""<br>&nbsp;<br>""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Album 2005/01
	#
	# <!-- Commentary on the picture -->
	#
	# <br>
	# Caption goes here
	# <center>
	# <!-- Image, maybe with link to original -->
	#
	caption = parseUtils.find_between_r(html,
"""<!-- Commentary on the picture -->

<br>""", 
"""<center>
<!-- Image, maybe with link to original -->""")

	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Album 2005/04
	#
	# <!-- Commentary on the picture -->
	# Caption goes here
	# <br>&nbsp;<br>
	#
	caption = parseUtils.find_between_r(html,
"""<!-- Commentary on the picture -->""", 
"""<br>&nbsp;<br>""")
	
	if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	#
	# Album 2006/07
	#
	# <!-- Comment -->
	#
	# <br>
	# <SPAN class="comment">The house has its own boat dock, with two great big boats.  Unfortunately they belong to a neighbor.</SPAN>
	#
	#
	#<br>&nbsp;<br>
	#<center>
	#<!-- Image, maybe with link to original -->
	#
	if not parsedHtml.body:
		sys.exit("cannot find parsedHtml.body %s" % parsedHtml) 

	captionElement = parsedHtml.body.find('span', attrs={'class':'comment'})
	if captionElement:
		caption = unicode(captionElement)
		if caption: return parseUtils.clean_caption(caption, htmlFile, html, parsedHtml)
	
	
	#
	# if we haven't figured out a caption at this point, we need
	# to improve the parsing.  print out some diagnostics and exit
	#
	
	if not caption:
		raise ParseError('no photo caption found', htmlFile, html, parsedHtml)
		
	return caption
