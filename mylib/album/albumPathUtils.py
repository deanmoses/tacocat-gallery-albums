#
# Utilities for dealing with Album paths
#

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

from PathValidationException import PathValidationException

#
# Validates path and returns list of path components
#
def parsePath(albumPath):
	'''
	Returns tuple of path components, throwing exception if path isn't valid

	Valid input formats:
	 2005 
	 2005/12-31
	 2005/12-31/snuggery

	Parameters
	----------
	albumPath : string
		path of album, like '2005' or '2005/12-31'
		or '2005/12-31/snuggery'

	Returns
	----------
	list like ['2001', '12-31', 'snuggery']
	
	Raises
	----------
	PathValidationException if album is NOT a valid album path
	'''
	logger.debug('Parsing album or photo path: [%s]' % albumPath)
	
	if not albumPath: raise PathValidationException(albumPath, 'cannot be empty')
	
	pathParts = albumPath.split('/')
	if len(pathParts) > 4: raise PathValidationException(albumPath, 'too many segments')
	
	#
	# validate year
	#
	year = pathParts.pop(0)
	if len(year) != 4: raise PathValidationException(albumPath, 'invalid year')
	try:
		int(year)
	except ValueError:
		raise PathValidationException(albumPath, 'invalid year')
	
	if len(pathParts) == 0:
		return [year]
		
	#
	# validate month-day
	#
	week = pathParts.pop(0)

	weekParts = week.split('-')
	if (len(weekParts) != 2): raise PathValidationException(albumPath, 'invalid week-day, too many or few dashes')
	
	#
	# validate month
	#
	month = weekParts.pop(0)
	if len(month) != 2: raise PathValidationException(albumPath, 'invalid month')
	try:
		int(month)
	except ValueError:
		raise PathValidationException(albumPath, 'invalid month')
	
	# validate day
	day = weekParts.pop(0)
	if len(day) != 2: raise PathValidationException(albumPath, 'invalid day')
	try:
		int(day)
	except ValueError:
		raise PathValidationException(albumPath, 'invalid day')
	
	if len(pathParts) == 0:
		return [year, week]
	
	photoOrSubAlbum = pathParts.pop(0)
	if len(pathParts) == 0:
		return [year, week, photoOrSubAlbum]

	subAlbum = pathParts.pop(0)
	return [year, week, photoOrSubAlbum, subAlbum]
	
#
# Error if it isn't a valid album or photo path
#
def validatePath(path):
	parsePath(path)

	
#
# Error if it isn't a valid photo path
#
def validatePhotoPath(photoPath):
	if len(parsePath(photoPath)) < 3: raise PathValidationException(photoPath, 'no photo on path')
	
#
# Transforms:
# 2005/12-31 into 2005
# or 
# 2005/12-31/snuggery into 2005/12-31
#
def parentPathFromChildPath(childAlbumPath):
	albumPathList = parsePath(childAlbumPath)
	albumPathList.pop()
	return '/'.join(albumPathList)
	
#
# Returns tuple of path components
#
def parseDiskPath(albumPath):
	'''
	Returns tuple of path components, throwing exception if path isn't valid

	Valid input formats:
	 2005 
	 2005/12/31
	 2005/12/31/snuggery

	Parameters
	----------
	albumPath : string
		path of album, like '2005' or '2005/12-31'
		or '2005/12-31/snuggery'

	Returns
	----------
	tuple: year ('2001'), week ('12-31'), and maybe subalbum ('snuggery')
	
	Raises
	----------
	PathValidationException if album is NOT a valid album path
	'''
	logger.debug('Parsing album disk path: %s' % albumPath)
	
	pathParts = albumPath.split('/')
	if len(pathParts) > 4: raise PathValidationException(albumPath, 'too many segments')
	
	#
	# validate year
	#
	year = pathParts.pop(0)
	if len(year) != 4: raise PathValidationException(albumPath, 'invalid year')
	try:
		int(year)
	except ValueError:
		raise PathValidationException(albumPath, 'invalid year')
	
	# validate month
	month = pathParts.pop(0)
	if len(month) != 2: raise PathValidationException(albumPath, 'invalid month')
	try:
		int(month)
	except ValueError:
		raise PathValidationException(albumPath, 'invalid month')
	
	# validate day
	day = pathParts.pop(0)
	if len(day) != 2: raise PathValidationException(albumPath, 'invalid day')
	try:
		int(day)
	except ValueError:
		raise PathValidationException(albumPath, 'invalid day')
	
	# create week string
	week = "%s-%s" % (month, day)
	
	# do we have a sub album?
	if (len(pathParts) == 1):
		subalbum = pathParts.pop(0)
		return year, week, subalbum
	else:
		return year, week
	
#
# Ensure we have a valid album disk path
#
def validateDiskPath(albumPath):
	'''
	Validate that albumPath is a valid album path.

	Parameters
	----------
	albumPath : string
		path of album, like '2005' or '2005/12-31'
		or '2005/12-31/snuggery'

	Raises
	----------
	Exception if album is NOT a valid album path
	'''
	parseDiskPath(albumPath)

#
# Transforms 2005/12/31/snuggery into 2005/12-31/snuggery
#
def albumPathFromDiskPath(albumDiskPath):
	albumPathTuple = parseDiskPath(albumDiskPath)
	return '/'.join(albumPathTuple)
