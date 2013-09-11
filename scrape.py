#!/usr/bin/env python
# program to scrape the static tacocat picture gallery albums, before the Menalto gallery software

#
# walkDirs.py has list of albums I will have to process by hand
#

# import third party libraries
import os
import sys
#import HTMLParser #not using yet
import argparse

# import my own local code
from mylib.Config import Config
from mylib.walkDirs import walkDirs 
from mylib.writeAlbum import writeAlbum

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

# scrape all the albums into Album objects in memory
albums = walkDirs(args.filterYears)

print """\n
------------------------------------------
----------- printing albums --------------
------------------------------------------"""

# print or write the albums
for album in albums:
	print '''\n-----------\n'''
	writeAlbum(album, args.doWriteToDisk)
