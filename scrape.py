#!/usr/bin/env python
# program to scrape static tacocat picture gallery, before the Menalto gallery software

#
# look in walkDirs.py for list of albums I will have to process by hand
#

# import third party libraries
import os
import sys
import HTMLParser #not using yet
import argparse

# import my own local code
import walkDirs
import writeAlbum

# parse command-line arguments
parser = argparse.ArgumentParser(description='Process tacocat gallery static HTML albums')
parser.add_argument('-years', dest='filterYears', nargs='*', help='years to process')
parser.add_argument('-write', dest='doWriteToDisk', action='store_const', const=True, help='write to disk instead of printing to screen')
args = parser.parse_args()

#
# constants
#
pixDir = '/home/deanmoses/themosii.com/pix/' # root of tacocat static HTML albums
outDir = '/home/deanmoses/scrape/output/'  # dir to write output to

# so I can read diagnostic output better
print """\n\n\n\n\n\n
------------------------------------------
----------- scraping albums --------------
------------------------------------------"""

# scrape all the albums into Album objects in memory
albums = walkDirs.walkDirs(pixDir, args.filterYears)

print """\n
------------------------------------------
----------- printing albums --------------
------------------------------------------"""

# print or write the albums
for album in albums:
	print '''\n-----------\n'''
	writeAlbum.writeAlbum(album, args.doWriteToDisk, outDir)
	
if (args.doWriteToDisk):
	print "I should write to disk, but that's not yet finished"
