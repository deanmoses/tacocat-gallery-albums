#
# Return Album as XML
#

# import third party libraries
import xml.etree.ElementTree as ET  # XML writer
import xml.dom.minidom

# import my own local code
from Config import Config

#
# Return specified album as an XML string
#
def toXml(album):
	'''
	Return specified album as an XML string
	
	Parameters
	----------
	album : Album
	   album to return as XML string
	'''
	
	#
	# create in-memory XML document representing album
	#
	
	a = ET.Element('album')
	a.set('year', album.year)
	a.set('name', album.name)
	
	if album.title:
		a.set('title', album.title)
		
	if album.caption:
		albumCaption = ET.SubElement(a, 'caption')
		albumCaption.text = album.caption
		
	for photo in sorted(album.photos):
		p = ET.Element('photo')
		p.set('name', photo.name)
		p.set('imageFile', photo.imageFile)
		if photo.title:
			p.set('title', photo.title)
			
		a.append(p)
	
	#
	# create pretty XML string
	#
	
	xmlstr = ET.tostring(a, encoding='utf8')
	xmlObj = xml.dom.minidom.parseString(xmlstr)
	pretty_xml_as_string = xmlObj.toprettyxml()
	
	return pretty_xml_as_string
	
