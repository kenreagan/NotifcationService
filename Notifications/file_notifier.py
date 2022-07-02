import os
import threading
from notification import BaseNotifier
# from abc import ABC, abstractmethod
from io import BytesIO
from exceptions import FileTooLargeError
import shutil
from concurrent.futures import ThreadPoolExecutor as process_pool
from logger import logger


ALLOWED_FILE_EXTENSIONS = [".zip", ".tar", ".doc", ".odt", ".docx", ".jpg", ".jpeg", ".png", ".mp3", '.py', '.mp4']

FILE_SIZE_LIMIT = 10 * 1024


class FileBaseClass:
	def __init__(
			self,
			owner=None,
			expiry_date=None,
			stream=None,
			filename=None):
		self.owner = owner
		self.expiry_date = expiry_date
		self.stream: BytesIO = stream or BytesIO()
		if filename is None:
			filename = getattr(stream, 'name', None)
			
			if filename is not None:
				filename = os.fsdecode(filename)
			else:
				filename = None
		
		filename = os.fsdecode(filename)

		if os.path.splitext(filename)[-1] in ALLOWED_FILE_EXTENSIONS:
			if os.path.getsize(filename) > FILE_SIZE_LIMIT:
				raise FileTooLargeError(f"The file size required is {FILE_SIZE_LIMIT!r} bytes")
			else:
				self.filename = filename		
		else:
			self.filename = None
	
		
	def save(self, destination, buffer_size=1):
		"""
			Save file for upload to the service
		"""
		
		status = True
		
		logger.info(f"🏃🏃🏃 Saving file to {destination.name} ...")
		while status:
			shutil.copyfileobj(self.stream, destination, buffer_size)
			status = False
		self.close_connection()
		return self
		
	def close_connection(self):
		self.stream.close()
		
	
	def __repr__(self):
		return f"{self.__class__.__qualname__}(filename={self.filename}, expiry={self.expiry_date}, owner={self.owner})"


# must have a File object
class FileNotifier(BaseNotifier):
	"""
		Handles Client File uploading to the server
	"""
	def dispatch(self):
		pass
		
		
if __name__ == '__main__':
	files = FileBaseClass(owner='lumuli', expiry_date='', stream=open('email_notifier.py'))
	print(files)
	
	files.save(open('/home/ken/projects/python/webdev/microservices/Myprojects/Notification/master.py', 'w'))
