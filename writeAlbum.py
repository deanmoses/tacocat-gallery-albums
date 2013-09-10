# import third party libraries
import xml.etree.ElementTree as ET  # XML writer
import xml.dom.minidom

#
# Write or print an individual album
#
def writeAlbum(album):
	'''
	Write or print an individual album
	
	Parameters
	----------
	album : Album
	   album to print or write
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
	# write XML document out
	#
	
	#ET.dump(a)
	xmlstr = ET.tostring(a, encoding='utf8')
	xmlObj = xml.dom.minidom.parseString(xmlstr)
	pretty_xml_as_string = xmlObj.toprettyxml()
	
	print pretty_xml_as_string
	
	#xmlFilename = '%s.%s' % (album.year, album.name)
	#historyET.write(xmlFilename,"UTF-8")