#
# Utilities for dealing with Album paths
#

#
# Returns tuple of path components
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
	tuple: year ('2001'), week ('12-31'), and maybe subalbum ('snuggery')
	
	Raises
	----------
	Exception if album is NOT a valid album path
	'''
	pathParts = albumPath.split('/')
	if len(pathParts) > 3: raise Exception('too many segments in %s' % albumPath)
	
	#
	# validate year
	#
	year = pathParts.pop(0)
	if len(year) != 4: raise Exception('year is not valid: %s' % albumPath)
	try:
		int(year)
	except ValueError:
		raise Exception('year is not valid: %s' % albumPath)
	
	# validate week (month-day)
	week = pathParts.pop(0)

	weekParts = week.split('-')
	
	#validate month
	month = weekParts.pop(0)
	if len(month) != 2: raise Exception('month is not valid: %s' % albumPath)
	try:
		int(month)
	except ValueError:
		raise Exception('month is not valid: %s' % albumPath)
	
	# validate day
	day = weekParts.pop(0)
	if len(day) != 2: raise Exception('day is not valid: %s' % albumPath)
	try:
		int(day)
	except ValueError:
		raise Exception('day is not valid: %s' % albumPath)
	
	# do we have a sub album?
	if (len(pathParts) == 1):
		subalbum = pathParts.pop(0)
		return year, week, subalbum
	else:
		return year, week
		
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
	Exception if album is NOT a valid album path
	'''
	pathParts = albumPath.split('/')
	if len(pathParts) > 4: raise Exception('too many segments in %s' % albumPath)
	
	#
	# validate year
	#
	year = pathParts.pop(0)
	if len(year) != 4: raise Exception('year is not valid: %s' % albumPath)
	try:
		int(year)
	except ValueError:
		raise Exception('year is not valid: %s' % albumPath)
	
	# validate month
	month = pathParts.pop(0)
	if len(month) != 2: raise Exception('month is not valid: %s' % albumPath)
	try:
		int(month)
	except ValueError:
		raise Exception('month is not valid: %s' % albumPath)
	
	# validate day
	day = pathParts.pop(0)
	if len(day) != 2: raise Exception('day is not valid: %s' % albumPath)
	try:
		int(day)
	except ValueError:
		raise Exception('day is not valid: %s' % albumPath)
	
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
	parsePath(albumPath)

#
# Transforms 2005/12/31/snuggery into 2005/12-31/snuggery
#
def albumPathFromDiskPath(albumDiskPath):
	albumPathTuple = parseDiskPath(albumDiskPath)
	return '/'.join(albumPathTuple)
	

#
# Transforms:
# 2005/12-31 into 2005
# or 
# 2005/12-31/snuggery into 2005/12-31
#
def parentPathFromChildPath(childAlbumPath):
	albumPathList = list(parsePath(childAlbumPath))
	albumPathList.pop()
	return '/'.join(albumPathList)
