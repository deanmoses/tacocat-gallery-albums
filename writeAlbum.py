import xml.etree.ElementTree as ET  # XML writer

#
# write an individual album out
#
def writeAlbum(album):
	# create XML document representing album
	a = ET.Element('album')
	a.set('year', album.year)
	if (album.title):
		a.set('title', album.title)
	if (album.caption):
		albumCaption = ET.SubElement(a, 'caption')
		albumCaption.text = album.caption
	for (photo) in sorted(album.photos):
		p = ET.Element('photo')
		p.set('name', photo.name)
		if (photo.title):
			p.set('title', photo.title)
		a.append(p)
	
	# write XML document out	
	ET.dump(a)
	xmlFilename = '%s.%s' % (album.year, album.name)
	#historyET.write(xmlFilename,"UTF-8")