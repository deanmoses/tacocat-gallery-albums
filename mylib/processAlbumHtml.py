#
# process album's index HTML file
#

# import external libraries
import sys

# import my own local code
import parseUtils
import processAlbumCaption
from ParseError import ParseError

#
# scrape album index HTML file for summary (the brief bit of optional info under the title)
#
def scrapeSummary(parsedHtml):
	"""
	Process album index HTML file, return summary
	
	Parameters
	----------
	parsedHtml : BeautifulSoup
		BeautifulSoup object representing parsed album index HTML file
		
	Returns
	----------
	string summary or '' if none
	"""

	summary = parsedHtml.title.text
	
	if summary:
		# we don't want album summaries like "January 1, 2002"
		stopwords = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
		for stopword in stopwords:
			if stopword in summary.lower():
				return ''
			
	return summary


#
# scrape album index HTML file for album caption
#
def scrapeCaption(htmlFile, html, parsedHtml):
	
	#
	# get caption
	#
	try:
		caption = processAlbumCaption.processAlbumCaption(htmlFile, html, parsedHtml)
	except AssertionError as e:
		url = htmlFile.replace('/home/deanmoses/themosii.com/', '')
		sys.exit("""\n\n
		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		photo caption error: %s 
		%s
		http://tacocat.com/%s
		\n\n
		%s
		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		""" % (e.message, htmlFile, url, html))
	
	return caption

#
# scrape the album's photo order by looking at the index HTML file's thumbnails
#
def scrapePhotoOrder(albumHtmlFile, html, parsedHtml):
	
	imageNames = []
	
	#
	# Album 2001/12
	#
	# <td align="center"> 
	#   <a href="html/felix_yet_again.htm">
	#       <img src="thumbnails/felix_yet_again.jpg" border="0" alt="felix_yet_again">
	#   </a>
	# </td>
	#
	for tdTag in parsedHtml.body.findAll('td', {"align" : "center"}):
		if not tdTag.a or not tdTag.a.img: continue # the captions are in cells just like this.  Skip them
		photoName = tdTag.a.img['alt']
		#imageName = imageSrc.rsplit('/', 1)[1] # from some/path/supper.jpg, get supper.jpg
		imageNames.append(photoName)
		
	if len(imageNames) > 0: return imageNames
	
	#
	# Album 2002/03/04
	#
	# <td style='padding:0in 0in 0in 0in'>
	#  <p class=MsoNormal align=center style='text-align:center'><a
	#  href="html/knitting.htm"><span style='text-decoration:none;text-underline:
	#  none'><img border=0 width=100 height=75 id="_x0000_i1029"
	#  src="thumbnails/knitting.jpg" alt=knitting></span></a></p>
	#  </td>
	#
	for tdTag in parsedHtml.body.findAll('td'):
		if tdTag.p:
			if tdTag.p.span:
				if tdTag.p.span.img:
					photoName = tdTag.p.span.img['alt']
					imageNames.append(photoName)
	
	if len(imageNames) > 0: return imageNames
	
	if len(imageNames) < 3:
		sys.exit('Got less than %s thumbs for album %s: %s' % (3, albumHtmlFile, imageNames))
		
	return imageNames
		