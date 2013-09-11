from Config import Config

#
# raised when album or photo HTML parsing fails, such can't find the caption
#
class ParseError(Exception):
	
	def __init__(self, value, htmlFile, html, parsedHtml):
		self.value = value
		self.htmlFile = htmlFile
		self.html = html
		self.parsedHtml = parsedHtml
		
	def __str__(self):
		url = self.htmlFile.replace(Config.webRoot, '')
		return """\n\n
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
%s
%s
http://tacocat.com/%s

-------------------- html page ----------------------

%s
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""" % (self.value, self.htmlFile, url, self.html)