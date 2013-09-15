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
def toFile(album, albumString, extension):
	'''
	Write specified string representing an Album to a file on disk.
	The string may be in XML or JSON or another format, 
	it's not the job of this method to know.
	
	Parameters
	----------
	album : Album
	   Album object, need this to figure out Album name and such to create filename
	
	albumString : string
		string representing an Album, to be written to disk
		
	extension
		file suffix 
		such as 'xml' or 'json'.  Do not include the preceding '.'
	'''
	
	# directory to write file to
	outDir = '%s%s/' % (Config.outDir, album.year)
	
	# full path to file
	filename = '%s%s.%s' % (outDir, album.name, extension)
	
	if os.path.isfile(filename):
		print "Not writing - file already exists: %s" % filename
	else:
		# make any of the parent dirs that haven't yet been created
		if not os.path.isdir(outDir): os.makedirs(outDir, 0755 )
		
		# write the file
		with open(filename, "w+") as f:
		    f.write(albumString)
		
		print "Wrote to %s" % filename