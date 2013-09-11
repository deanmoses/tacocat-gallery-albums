# import third party libraries
import os
import xml.etree.ElementTree as ET  # XML writer
import xml.dom.minidom

# import my own local code
from Config import Config

#
# Write or print an individual album
#
def writeAlbum(album, doWriteToDisk):
	'''
	Write or print an individual album
	
	Parameters
	----------
	album : Album
	   album to print or write
	doWriteToDisk : boolean
		True: write to disk instead of printing to screen
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
	
	print pretty_xml_as_string
	
	#
	# write XML to file
	#
	
	if doWriteToDisk:
		# directory to write file to
		outDir = '%s%s/' % (Config.outDir, album.year)
		
		# full path to file
		xmlFilename = '%s%s.xml' % (outDir, album.name)
		
		if os.path.isfile(xmlFilename):
			print "Not writing - file already exists: %s" % xmlFilename
		else:
			# make any of the parent dirs that haven't yet been created
			if not os.path.isdir(outDir): os.makedirs(outDir, 0755 )
			
			# write the file
			with open(xmlFilename, "w+") as f:
			    f.write(pretty_xml_as_string)
			
			print "Wrote XML to: %s" % xmlFilename
	
