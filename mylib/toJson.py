#
# Return Album as JSON
#

# import third party libraries
import json

# handles encoding an Album and its child Photo objects as JSON
class AlbumEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

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