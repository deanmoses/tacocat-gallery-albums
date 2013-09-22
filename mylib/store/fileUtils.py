#
# Write Album to a file on disk
#

# import third party libraries
import os

# import my own local code
from Config import Config

#
# Write specified string representing an Album to a file on disk.
# Error if the file already exists.
# Creates intervening directories if needed.
#
def createFile(albumPath, albumString):
	'''
	Write specified string representing an Album to a file on disk.
	The string may be in XML or JSON or another format, 
	it's not the job of this method to know.
	
	Parameters
	----------
	albumPath : string
	   full file path + filename to where album should be written to disk
	
	albumString : string
		string representing an Album, will become contents of file on disk
	'''
	# make any of the parent dirs that haven't yet been created
	parentDir = os.path.dirname(os.path.realpath(albumPath))
	if not os.path.isdir(parentDir): os.makedirs(parentDir, 0755 )
	
	# write the file
	with open(albumPath, "w+") as f:
	    f.write(albumString)

#
# Update existing file on disk.  
# Error if it doesn't already exist.
#
def updateFile(albumPath, albumString):
	'''
	Write specified string representing an Album to a file on disk.
	The string may be in XML or JSON or another format, 
	it's not the job of this method to know.
	
	Parameters
	----------
	albumPath : string
	   full file path + filename to where album should be written to disk
	
	albumString : string
		string representing an Album, will become contents of file on disk
	'''
	assert os.path.isfile(albumPath), "File does not exist: %s" % albumPath
	
	# write the file
	# r+ = open existing file for read or write, so I probably don't have to check existence above
	with open(albumPath, "r+") as f:
	    f.write(albumString)
	
	
#
# Retrieve album string from path
#
def readFile(albumPath):
	with open(albumPath) as f: return f.read()
	
