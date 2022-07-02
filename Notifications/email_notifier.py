from notification import BaseNotifier
import smtplib


class EmailNotifier(BaseNotifier):
	def prepare_service(self):
		pass
		
	def validate_message(self):
		pass
		
	def prepare_socket(self):
		pass
		
	def dispatch(self):
		pass
