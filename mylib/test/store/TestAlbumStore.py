import unittest, nose
import os, sys
from store.AlbumStore import AlbumStore
from album.NotFoundException import NotFoundException
from album.AlbumException import AlbumException

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

class TestAlbumStore(unittest.TestCase):
	
	#
	#
	#
	def test_getAlbum(self):
		# test getting root album
		rootAlbumPaths = [None, '', '/']
		for path in rootAlbumPaths:
			logger.debug('testing getAlbum() with root path: [%s]', path)
			album = AlbumStore.getAlbum(path)
			if not album:
				self.fail('Empty album: %s' % path)
			if (not hasattr(album, 'title')) or len(album.title) <= 0:
				self.fail('Empty album [%s] title' % path)
			if (not hasattr(album, 'pathComponent')):
				self.fail('No album pathComponent: %s' % path)
		
		# test successful album retrieval
		goodAlbumPaths = [
			'2001',
			'/2001',
			'2002',
			'/2002',
			'2001/',
			'2002/',
			'2001/12-13/',
			'/2001/12-31/',
			'2001/12-31//',
			'2004/12-12/first_meal'
		]
		
		for path in goodAlbumPaths:
			logger.debug('testing getAlbum() with good path: [%s]', path)
			album = AlbumStore.getAlbum(path)
			if not album:
				self.fail('Empty album: %s' % path)
			if (not hasattr(album, 'title')) or len(album.title) <= 0:
				self.fail('Empty album title: %s' % path)
			if (not hasattr(album, 'pathComponent')):
				self.fail('No album pathComponent: %s' % path)
			self.assertEquals(path.strip('/'), album.pathComponent)
			self.assertTrue(len(album.pathComponent) >= 4)
			
		# test fail album retrieval
		badAlbumPaths = [
			'a',
			'asl;dfjk',
			'200000',
			'2000.00',
			'2001/12',
			'2001/12/',
			'2001/12/31'
			'2001/12/31/',
			'2001/123-31/',
			'2001/12-312/',
			'2001/aa-31/',
			'2001/aa-bb/'
		]
		
		for path in badAlbumPaths:
			try:
				logger.debug('testing getAlbum(%s) (bad path)', path)
				AlbumStore.getAlbum(path)
				self.fail('getAlbum(%s) should not have succeeded' % path)
			except AssertionError, inst:
				raise inst
			except AlbumException, inst:
				logger.debug('getAlbum(%s) failed as expected: %s' % (path, str(inst)))
		
		
	#
	#
	#
	def test_getPhoto(self):		
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
			logger.debug('testing getAlbu() with good path: %s', path)
			photo = AlbumStore.getPhoto(path)
			if not photo:
				self.fail('Empty photo: %s' % path)
			if (not hasattr(photo, 'title')) or len(photo.title) <= 0:
				self.fail('Empty photo title: %s' % path)
			if (not hasattr(photo, 'pathComponent')) or len(photo.pathComponent) <= 0:
				self.fail('Empty photo title: %s' % path)	
				
		for path in badPhotoPaths:
			try:
				logger.debug('testing getPhoto() with bad path: %s', path)
				AlbumStore.getPhoto(path)
				self.fail('getPhoto(%s) should not have succeeded' % path)
			except AssertionError, inst:
				raise inst
			except AlbumException, inst:
				logger.debug('getPhoto(%s) failed as expected: %s' % (path, str(inst)))
	
	
	#
	#
	#
	def test_updatePhotoFromDict(self):
		path = '2001/12-13/harriet'
		photo = AlbumStore.getPhoto(path)
		originalTitle = photo.title
		originalDescription = photo.description
		
		AlbumStore.updatePhotoFromDict(path, {'title': 'title1','description': 'description1'})
		photo = AlbumStore.getPhoto(path)
		self.assertTrue(photo.title == 'title1')
		self.assertTrue(photo.description == 'description1')
		
		AlbumStore.updatePhotoFromDict(path, {'description': 'description2'})
		photo = AlbumStore.getPhoto(path)
		self.assertTrue(photo.title == 'title1')
		self.assertTrue(photo.description == 'description2')
		
		AlbumStore.updatePhotoFromDict(path, {'title': 'title3'})
		photo = AlbumStore.getPhoto(path)
		self.assertTrue(photo.title == 'title3')
		self.assertTrue(photo.description == 'description2')
		
		# should return the photo back to original state
		AlbumStore.updatePhotoFromDict(path, {'title': originalTitle,'description': originalDescription})
		photo = AlbumStore.getPhoto(path)
		self.assertTrue(photo.title == originalTitle)
		self.assertTrue(photo.description == originalDescription)
		
		# try a bunch of bad photo updates
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
				logger.debug('test updating bad photo %s' % path)
				AlbumStore.updatePhotoFromDict(path, attrs)
				self.fail('Should not have succeeded: %s, attributes: %s' % (path, attrs))
			except AssertionError, inst:
				raise inst
			except AlbumException, inst:
				logger.debug('bad photo update for photo [%s] failed as expected.  Failure: %s' % (path, str(inst)))


	#
	# Assert that album exists and can be updated
	#
	def assertAlbumExists(self, album):
		# parent album should now have this album's thumbnail info
		parentAlbum = AlbumStore.getParentAlbum(album.pathComponent)
		thumb = parentAlbum.getChildAlbumThumbnail(album.pathComponent)
		self.assertTrue(thumb.pathComponent == album.pathComponent)
	
		# retrieve should now succeed
		savedAlbum = AlbumStore.getAlbum(album.pathComponent)
		self.assertTrue(savedAlbum.pathComponent == album.pathComponent)
	
		# update should now succeed
		originalDescription = album.description
		album.description = "caption #2"
		AlbumStore.updateAlbum(album)
	
		# test that album was actually updated
		album = AlbumStore.getAlbum(album.pathComponent)
		self.assertEquals("caption #2", album.description)
		
		# put album back to original state
		album.description = originalDescription
		AlbumStore.updateAlbum(album)
		album = AlbumStore.getAlbum(album.pathComponent)
		self.assertEquals(originalDescription, album.description)
		
	#
	# Assert album does not exist
	#
	def assertAlbumDoesNotExist(self, album):
		# parent album should no longer have this album's thumbnail info
		parentAlbum = AlbumStore.getParentAlbum(album.pathComponent)
		try:
			parentAlbum.getChildAlbumThumbnail(album.pathComponent)
			self.fail('Should not have been able to retrieve thumb of deleted album')
		except AssertionError, inst:
			raise inst
		except AlbumException, inst:
			logger.debug('Got exception as expected retrieving thumbnail of deleted album: %s' % str(inst))

		# retrieve should now fail
		try:
			AlbumStore.getAlbum(album.pathComponent)
			self.fail("getAlbum() should have failed on on nonexistent album")
		except AssertionError, inst:
			raise inst
		except AlbumException, inst:
			logger.debug('Got exception as expected on getAlbum: %s' % str(inst))

		# update should now fail
		try:
			AlbumStore.updateAlbum(album)
			self.fail("updateAlbum() should have failed on nonexistent album")
		except AssertionError, inst:
			raise inst
		except AlbumException, inst:
			logger.debug('Got exception as expected on updateAlbum: %s' % str(inst))

		# delete should now fail
		try:
			AlbumStore.deleteAlbum(album.pathComponent)
			self.fail("deleteAlbum() should have failed on nonexistent album")
		except AssertionError, inst:
			raise inst
		except AlbumException, inst:
			logger.debug('Got exception as expected on deleteAlbum: %s' % str(inst))

				
	#
	# Test album create (and delete)
	#
	def test_createAlbum(self):
		# create a fake test album
		album = AlbumStore.newAlbum('2001/12-01', description='caption #1')
		self.assertAlbumDoesNotExist(album)
		AlbumStore.createAlbum(album)
		self.assertAlbumExists(album)
		AlbumStore.deleteAlbum(album.pathComponent)
		self.assertAlbumDoesNotExist(album)
		
		# create a fake year album
		yearAlbum = AlbumStore.newAlbum('1977')
		self.assertAlbumDoesNotExist(yearAlbum)
		AlbumStore.createAlbum(yearAlbum)
		self.assertAlbumExists(yearAlbum)
		
		# create a fake day album under fake year
		dayAlbum = AlbumStore.newAlbum('1977/01-01', description='caption A')
		self.assertAlbumDoesNotExist(dayAlbum)
		AlbumStore.createAlbum(dayAlbum)
		self.assertAlbumExists(dayAlbum)
		
		# delete fake day album
		AlbumStore.deleteAlbum(dayAlbum.pathComponent)
		self.assertAlbumDoesNotExist(dayAlbum)
		
		# delete fake year album
		AlbumStore.deleteAlbum(yearAlbum.pathComponent)
		self.assertAlbumDoesNotExist(yearAlbum)

		
	
if __name__ == '__main__':
	unittest.main()