# import external libraries
import sys
from bs4 import BeautifulSoup, Comment # BeautifulSoup HTML parsing module I installed locally

# import my own local code
from parseUtils import find_between

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
	# some photos genuinely don't have captions
	#
	noCaptions = [
		'2001/12/13/',
		'2001/12/14/',
		'2001/12/16/',
		'2001/12/23/html/eyes_wide_open.htm',
		'2001/12/23/html/felix_and_the_armpit.htm',
		'2001/12/23/html/lulix1.htm',
		'2001/12/23/html/lulix2.htm',
		'2001/12/23/html/lulix3.htm',
		'2001/12/23/html/molix_sleeping.htm',
		'2001/12/23/html/molulix.htm',
		'2001/12/31/html/felix1.htm',
		'2001/12/31/html/felix2.htm',
		'2001/12/31/html/felix3.htm',
		'2001/12/31/html/felix4.htm',
		'2001/12/31/html/felix_yet_again.htm',
		'2001/12/31/html/francoisix1.htm',
		'2001/12/31/html/francoisix2.htm',
		'2001/12/31/html/francoisix3.htm',
		'2001/12/31/html/francoisix4.htm',
		'2001/12/31/html/grandma_francois.htm',
		'2001/12/31/html/king_of_the_swingers.htm',
		'2001/12/31/html/the_thinker.htm',
		'2001/12/31/html/zonked.htm'

	]
	for noCaption in noCaptions:
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
""" % (htmlFile, htmlFile.replace('/home/deanmoses/themosii.com/', ''), html))
		
	return caption
