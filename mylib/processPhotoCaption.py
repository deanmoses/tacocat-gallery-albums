# import external libraries
import sys

# import my own local code
from parseUtils import find_between
from config import Config

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
	# LView Pro albums circa 2001 have HTML like this:
	#
	# <!--
	# File: C:\Documents and Settings\moses.MOSESREMOTE\My Documents\My Pictures\tacocat\felix\2001.12.17-23\raw_images\maman_dans_la_cuisine.txt
	# -->
	# While Lucie kept Felix from starving, Francoise kept Lucie from starving. 
	# <p>
	# <center>
	# <table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="2" width="200">
	#
	caption = find_between(html, '-->', """<P>
<CENTER>
<TABLE border="0" cellpadding="0" cellspacing="2" width="200" bgcolor="#FFFFFF" >""")

	if caption: return caption

	#
	# LView Pro albums circa 2001 can also have HTML like this:
	#
	# </TABLE>
	# </CENTER>
	# <P>
	# <P>
	# Alicia gives Lucie, Moses, and Felix a lesson in how to feed from a pinky.
	# <P>
	# <CENTER>
	# <TABLE border="0" cellpadding="0" cellspacing="2" width="200" bgcolor="#FFFFFF" >
	#
	caption = find_between(html, 
"""</TABLE>
</CENTER>
<P>
<P>""", 
"""<P>
<CENTER>
<TABLE border="0" cellpadding="0" cellspacing="2" width="200" bgcolor="#FFFFFF" >
""")

	if caption: return caption



	#
	# if we haven't figured out a caption at this point, we need
	# to improve the parsing.  print out some diagnostics and exit
	#
	
	if not caption:
		sys.exit("""\n\n
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cannot find caption for photo 
%s
http://tacocat.com/%s
\n\n
%s
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""" % (htmlFile, htmlFile.replace(Config.webRoot, ''), html))
		
	return caption
