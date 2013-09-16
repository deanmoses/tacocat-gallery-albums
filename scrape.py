#!/usr/bin/env python
# program to scrape the static tacocat picture gallery albums, before the Menalto gallery software

#
# walkDirs.py has list of albums I will have to process by hand
#

# import third party libraries
import os
import sys
import argparse # for parsing command-line arguments to this program

# import my own local code
from mylib.Config import Config
from mylib.walkDirs import walkDirs 
from mylib.toXml import toXml
from mylib.toJson import toJson
from mylib.toFile import toFile

# parse command-line arguments
parser = argparse.ArgumentParser(description='Process tacocat gallery static HTML albums')
parser.add_argument('-album', dest='albumFilter', required=True, nargs=1, help='album to process, like -album 2001/12/31/ or -album 2001 to process all albums in 2001')
parser.add_argument('-verbose', dest='verbose', action='store_const', const=True, help='output more detailed information')
parser.add_argument('-write', dest='doWriteToDisk', action='store_const', const=True, help='write to disk instead of printing to screen')
parser.add_argument('-f', dest='overwriteFiles', action='store_const', const=True, help='overwrite existing files')
args = parser.parse_args()

if args.verbose:
	Config.verbose = True

albumFilter = args.albumFilter[0]
if len(albumFilter) < 4 or not albumFilter[:4].isdigit():
	sys.exit('-album must start with a 4 digit year.  Intead got %s' % albumFilter[:4])

# so I can read diagnostic output better
print """\n\n\n\n\n\n
------------------------------------------
----------- scraping albums --------------
------------------------------------------"""

# scrape the albums into Album objects in memory
albums = walkDirs(albumFilter)

print """\n
------------------------------------------
----------- printing albums --------------
------------------------------------------"""

# print or write the albums
for album in albums:
	# turn album into text string
	#albumString = toXml(album)
	albumString = toJson(album)
	
	# full path to write album file to
	albumPath = '%s%s/album.json' % (Config.outDir, album.pathComponent)
	
	if (args.doWriteToDisk):
		# write album text string to disk
		toFile(albumPath, albumString, args.overwriteFiles)
	else:
		print albumString
		print 'Would have written to: %s' % albumPath
		
	print '''\n-----------\n'''
