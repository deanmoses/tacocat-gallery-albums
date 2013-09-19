#
# Encode and decode Albums to/from JSON
#

# import third party libraries
import json

# import my own code
from Album import Album
from Photo import Photo
from Image import Image
from AlbumThumbnail import AlbumThumbnail
from YearAlbum import YearAlbum

# handles encoding an Album and its child Photo objects as JSON
class AlbumEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

# handles decoding JSON into objects
def albumDecoder (dict):
	if 'fullSizeImage' in dict and not 'creationTimestamp' in dict:
		return Photo(dict)
	elif 'height' in dict:
		return Image(dict)
	elif 'creationTimestamp' in dict and not 'children' in dict and not 'description' in dict:
		return AlbumThumbnail(dict)
	elif 'pathComponent' in dict and '/' not in dict['pathComponent']:
		return YearAlbum(dict)
	elif 'creationTimestamp' in dict and 'children' in dict:
		return Album(dict)
	else:
		return dict

#
# Return specified Album as a JSON string
#
def toJson(album):
	'''
	Return specified Album as a JSON string
	
	Parameters
	----------
	album : Album
	   album to return as JSON string
	
	Return
	----------
	JSON string representing album
	'''
	
	jsonString = json.dumps(album, sort_keys=True,
	               indent=4, cls=AlbumEncoder, separators=(',', ': '))
	
	return jsonString

#
# Return specified JSON string as an Album
#
def fromJson(jsonString):
	'''
	Return specified JSON string as an Album object
	
	Parameters
	----------
	jsonString : string
	   JSON string representing an Album
	
	Return
	----------
	Album object
	'''
	
	return json.loads(jsonString, object_hook=albumDecoder)