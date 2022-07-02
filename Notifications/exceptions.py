class FileTooLargeError(Exception):

	def __init__(self, message):
		self.error_message = message
		
		
	def __repr__(self):
		return f"{self.error_message}"
