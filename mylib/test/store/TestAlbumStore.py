import unittest, nose
import os, sys
from store.AlbumStore import AlbumStore

class TestAlbumStore(unittest.TestCase):
	
	def test_getPhoto(self):
		#print "path: %s" % sys.path
		
		goodPhotoPaths = [
			'2001/12-13/harriet',
			'2001/12-13/very_first_picture_ever.jpg',
			'2001/12-31/felix1',
			'2002/07-11/hat',
			'2004/12-12/first_meal/eat1'
		]
		badPhotoPaths = [
			None, '', ' ', '/2005', '2005/', 
			'2005/12-31', '2005/12-31/', '2005/12/31',
			'/2001/12-13/very_first_picture_ever.jpg',
			'2001/12-13/harriet/',
		]
		
		for path in goodPhotoPaths:
			photo = AlbumStore.getPhoto(path)
			if not photo:
				self.fail('Empty photo: %s' % path)
			if len(photo.title) <= 0:
				self.fail('Empty photo title: %s' % path)
			if len(photo.pathComponent) <= 0:
				self.fail('Empty photo title: %s' % path)	
				
		for path in badPhotoPaths:
			try:
				AlbumStore.getPhoto(path)
				self.fail('Should not have succeeded: %s' % path)
			except Exception:
				pass
	
	
	def test_updatePhoto(self):
		goodUpdates = { 
			'2001/12-13/harriet': {
				'title': 'aaaa',
				'description': 'bbbb'
			},
			'2001/12-13/harriet': {
				'description': 'cccc'
			},
			'2001/12-13/harriet': {
				'title': 'dddd'
			}
			}
		for path, attrs in goodUpdates.iteritems():
			AlbumStore.updatePhoto(path, attrs)
		
		badUpdates = {
			'/2001/12-13/harrietcccc/': {
				'title': 'eeee',
				'description': 'ffff'
			},
			'2001/12/13/harriet': {
				'title': 'eeee',
				'description': 'ffff'
			},
			'/2001/12-13/harriet': {
				'title': 'eeee',
				'description': 'ffff'
			},
			'2001/12-13/harriettttt': {
				'title': 'eeee',
				'description': 'ffff'
			},
			'2001/12-13/harriet': {
				'noSuchProp': 'gggg',
				'title': 'hhh',
				'description': 'iiiii'
			},
			'2001/12-13/harriet': {
			},
			'2001/12-13/harriet': None,
			'2001/12-13/harriet': [],
			'2001/12-13/harriet': {
				'title': ''
			},
			'2001/12-13/harriet': {
				'title': None
			}
			}
		for path, attrs in badUpdates.iteritems():
			try:
				AlbumStore.updatePhoto(path, attrs)
				self.fail('Should not have succeeded: %s, attributes: %s' % (path, attrs))
			except Exception:
				pass

	#
	# Test album and photo create and update
	#
	def test_creation(self):
		album = AlbumStore.newAlbum('2001/12-01', 'December 12', 'Some caption')
		AlbumStore.createAlbum(album)
		
		
		
	
if __name__ == '__main__':
	unittest.main()