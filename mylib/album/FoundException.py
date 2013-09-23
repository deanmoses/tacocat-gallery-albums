from AlbumException import AlbumException

'''
Raised when an Album or Photo is found and shouldn't be
'''
class FoundException(AlbumException):
	def __init__(self, path):
		fullMessage = 'Found: %s' % (path)
		
		# Call the base class constructor with the parameters it needs
		AlbumException.__init__(self, fullMessage)