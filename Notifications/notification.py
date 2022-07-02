import threading
from collections import namedtuple, deque
from abc import abstractmethod, ABC


class BaseNotifier(ABC):
	def __init__(self, recepient, message, sender, protocol):	
		self.recepient = recepient
		self.message = message
		self.sender = sender
		self.protocol = protocol
		
	@abstractmethod
	def dispatch(self):
		pass

