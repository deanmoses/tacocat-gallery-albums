#!/usr/bin/env python
# program to scrape the static tacocat picture gallery albums, before the Menalto gallery software

#
# walkDirs.py has list of albums I will have to process by hand
#

# import third party libraries
import os
import sys
#import HTMLParser #not using yet
import argparse # for parsing command-line arguments to this program

# import my own local code
from mylib.Config import Config
from mylib.walkDirs import walkDirs 
from mylib.toXml import toXml
from mylib.toJson import toJson
from mylib.toFile import toFile

# parse command-line arguments
parser = argparse.ArgumentParser(description='Process tacocat gallery static HTML albums')
parser.add_argument('-verbose', dest='verbose', action='store_const', const=True, help='output more detailed information')
parser.add_argument('-years', dest='filterYears', nargs='*', help='years to process')
parser.add_argument('-write', dest='doWriteToDisk', action='store_const', const=True, help='write to disk instead of printing to screen')
args = parser.parse_args()

if args.verbose:
	Config.verbose = True


# so I can read diagnostic output better
print """\n\n\n\n\n\n
------------------------------------------
----------- scraping albums --------------
------------------------------------------"""

# scrape the albums into Album objects in memory
albums = walkDirs(args.filterYears)

print """\n
------------------------------------------
----------- printing albums --------------
------------------------------------------"""

# print or write the albums
for album in albums:
	# create XML string
	#albumString = toXml(album)
	albumString = toJson(album)
	if (args.doWriteToDisk):
		# write string to disk
		fileExtension = 'json'
		toFile(album, albumString, fileExtension)
	else:
		print albumString
		
	print '''\n-----------\n'''
	
if (not args.doWriteToDisk):
	print 'Nothing written to disk.'
