from AlbumException import AlbumException

'''
Raised when path to an album or a photo isn't valid
'''
class PathValidationException(AlbumException):
	def __init__(self, path, message):
		fullMessage = '%s: %s' % (path, message)
		
		# Call the base class constructor with the parameters it needs
		AlbumException.__init__(self, fullMessage)