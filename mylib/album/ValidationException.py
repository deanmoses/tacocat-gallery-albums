'''
Raised when an Album or Photo isn't valid for saving
'''
class ValidationException(Exception):
	def __init__(self, path, field, message):

		fullMessage = '%s: %s is invalid: %s' % (path, field, message)
		
		# Call the base class constructor with the parameters it needs
		Exception.__init__(self, fullMessage)
