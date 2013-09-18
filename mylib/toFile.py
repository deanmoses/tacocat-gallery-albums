#
# Write Album to a file on disk
#

# import third party libraries
import os

# import my own local code
from Config import Config

#
# Write specified string representing an Album to a file on disk.
# The string may be in XML or JSON or another format, 
# it's not the job of this method to know.
#
def toFile(albumPath, albumString, overwriteFiles=True):
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
		
	overwriteFiles : boolean
		true: overwrite existing files
	'''
	
	if not overwriteFiles and os.path.isfile(albumPath):
		print "    Not writing - file already exists: %s" % albumPath
	else:
		# make any of the parent dirs that haven't yet been created
		parentDir = os.path.dirname(os.path.realpath(albumPath))
		if not os.path.isdir(parentDir): os.makedirs(parentDir, 0755 )
		
		# write the file
		with open(albumPath, "w+") as f:
		    f.write(albumString)

#
# Retrieve album string from path
#
def fromFile(albumPath):
	albumString = None
	
	with open(albumPath) as f:
		albumString = f.read()
	
	return albumString
	
