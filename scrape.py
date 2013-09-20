#!/usr/bin/env python
'''
Program to scrape the static tacocat picture gallery albums
2001-2006 before the Menalto gallery PHP software.

walkDirs.py has list of albums I will have to process by hand

For help running it, call ./scrape.py -h
'''

# import third party libraries
import os
import sys
import argparse # for parsing command-line arguments to this program

# make all the python files in mylib available to be imported w/o referencing 'mylib'
mylibDir = '%s' % (os.getcwd() + '/mylib')
sys.path.append(mylibDir)

# import my own local code
from Config import Config
from scraper.walkDirs import walkDirs

# parse command-line arguments
parser = argparse.ArgumentParser(description='Process tacocat gallery static HTML albums')
parser.add_argument('-album', dest='albumFilter', required=True, nargs=1, help='album to process, like -album 2001/12/31/ or -album 2001 to process all albums in 2001')
parser.add_argument('-verbose', dest='verbose', action='store_const', const=True, help='output more detailed information')
parser.add_argument('-write', dest='doWriteToDisk', action='store_const', const=True, help='write to disk instead of printing to screen')
args = parser.parse_args()

# use command-line args
Config.verbose = args.verbose
Config.doWriteToDisk = args.doWriteToDisk

albumFilter = args.albumFilter[0]
if len(albumFilter) < 4 or not albumFilter[:4].isdigit():
	sys.exit('-album must start with a 4 digit year.  Intead got %s' % albumFilter[:4])
	
# scrape the albums
walkDirs(albumFilter)
