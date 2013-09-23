from AlbumException import AlbumException

'''
Raised when a thumbnail isn't found on a parent album
'''
class ThumbnailNotFoundException(AlbumException):
	def __init__(self, parentAlbumPath, childAlbumPath):
		fullMessage = 'Album [%s]: did not find thumbnail for child album [%s]' % (parentAlbumPath, childAlbumPath)
		
		# Call the base class constructor with the parameters it needs
		AlbumException.__init__(self, fullMessage)