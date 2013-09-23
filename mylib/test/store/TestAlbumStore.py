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
			logger.debug('testing getPhoto() with good path: %s', path)
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
				self.fail('Should not have succeeded: %s' % path)
			except AssertionError, inst:
				raise inst
			except AlbumException, inst:
				logger.debug('bad photo retrieve for photo [%s] failed as expected.  Failure: %s' % (path, str(inst)))
	
	
	#
	#
	#
	def test_updatePhotoFromDict(self):
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
			logger.debug('test updating good photo %s' % path)
			AlbumStore.updatePhotoFromDict(path, attrs)
		
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
	# Test album create (and delete)
	#
	def test_createAlbum(self):
		# create a fake test album, not yet saved to disk
		album = AlbumStore.newAlbum('2001/12-01', 'December 12', 'caption #1')
				
		# retrieving a nonexistent album should fail
		try:
			AlbumStore.getAlbum(album.pathComponent)
			self.fail("This album should not exist")
		except AssertionError, inst:
			raise inst
		except AlbumException, inst:
			logger.debug('Got exception as expected on getAlbum: %s' % str(inst))
		
		# updating a nonexistent album should fail
		try:
			AlbumStore.updateAlbum(album)
			self.fail("This album should not exist")
		except AssertionError, inst:
			raise inst
		except AlbumException, inst:
			logger.debug('Got exception as expected on updateAlbum: %s' % str(inst))
			
		# deleting a nonexistent album should fail
		try:
			AlbumStore.deleteAlbum(album.pathComponent)
			self.fail("This album should not exist")
		except AssertionError, inst:
			raise inst
		except AlbumException, inst:
			logger.debug('Got exception as expected on deleteAlbum: %s' % str(inst))
			
		
		# create album should succeed
		AlbumStore.createAlbum(album)
		
		# parent album should now have this album's thumbnail info
		parentAlbum = AlbumStore.getParentAlbum(album.pathComponent)
		thumb = parentAlbum.getChildAlbumThumbnail(album.pathComponent)
		self.assertTrue(thumb.pathComponent == album.pathComponent)
		
		# retrieve should now succeed
		savedAlbum = AlbumStore.getAlbum(album.pathComponent)
		self.assertTrue(savedAlbum.pathComponent == album.pathComponent)
		
		# update should now succeed
		album.description = "caption #2"
		AlbumStore.updateAlbum(album)
		
		# test that album was actually updated
		album = AlbumStore.getAlbum(album.pathComponent)
		self.assertEquals("caption #2", album.description)
		
		# delete should now succeed
		AlbumStore.deleteAlbum(album.pathComponent)
		
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
		
		
	
if __name__ == '__main__':
	unittest.main()