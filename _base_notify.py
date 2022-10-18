from abc import ABC, abstractmethod
import os
from io import BytesIO
# from exceptions import FileTooLargeError
import shutil
from logger import logger


ALLOWED_FILE_EXTENSIONS = [".zip", ".tar", ".doc", ".odt", ".docx", ".jpg", ".jpeg", ".png", ".mp3", '.py', '.mp4']

FILE_SIZE_LIMIT = 10 * 1024


class BaseNotifier(ABC):
    def __init__(self, message, sender, recepient, protocol):
        self.message: str = message
        self.sender: str = sender
        self.recepient: str = recepient
        self.protocol = protocol
        self.status: bool = False
    
    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def serve_forever():
        pass


class FileBaseClass:
    def __init__(self, owner=None, expiry_date=None, stream=None, filename=None):
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
