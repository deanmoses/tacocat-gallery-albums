from AlbumException import AlbumException

'''
Raised when an Album or Photo isn't found
'''
class NotFoundException(AlbumException):
	def __init__(self, path):
		fullMessage = 'Not found: %s' % (path)
		
		# Call the base class constructor with the parameters it needs
		AlbumException.__init__(self, fullMessage)