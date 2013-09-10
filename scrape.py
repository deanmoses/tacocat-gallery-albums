#!/usr/bin/env python
# program to scrape static tacocat picture gallery, before the Menalto gallery software

#
# TODO BY HAND:
# pix/1999/ (all subalbums)
# pix/2001/07/ultrasound/
# pix/2001/09/bellytutu/
# pix/2001/10/doughboy/
# pix/2001/10/mermaid/
# pix/2003/12/ultrasound_bastille/
# pix/2004/04/08/
# pix/2005/12/01/
# pix/2005/12/22/
#

# import third party libraries
import os
import sys
import HTMLParser

# import my own local code
import walkDirs
import writeAlbum

#
# if a year was passed in as a command-line argument, filter by it
#
filterYear = None
if len(sys.argv) >= 2:
	filterYear = sys.argv[1]

#
# constants
#
pixDir = '/home/deanmoses/themosii.com/pix/'
outfileName = '/home/deanmoses/scrape/output.xml'

# so I can read diagnostic output better
print """\n\n\n\n\n\n
------------------------------------------
----------- scraping albums --------------
------------------------------------------"""

# scrape all the albums into Album objects in memory
albums = walkDirs.walkDirs(pixDir, filterYear)

print """\n
------------------------------------------
----------- printing albums --------------
------------------------------------------"""

# print or write the albums
for album in albums:
	print '''\n-----------\n'''
	writeAlbum.writeAlbum(album)
