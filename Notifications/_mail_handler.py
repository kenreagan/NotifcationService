from email.message import EmailMessage
import mimetypes
from _base_notify import BaseNotifier
from email.parser import Parser, BytesParser
from email.policy import default
from App.databasemanager import DatabaseContextManager
from App.models import User, Task
from logger import logger
import os

# email_re = re.compile(r'([a-z]*)(\@gmail.com)')

MAIN_SENDER_EMAIL = "lumulikenreagan@gmail.com" # replace with environment Variable


class BaseValidator(ABC):
    def __init__(self):
        self.det = None

    def set_det(self, owner, detail):
        self.det = f"_{self.detail}"

    def __set__(self, instance, value):
        self.validate()
        setattr(instance, self.det, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.det)

    @abstractmethod
    def validate(self):
        pass

class EmailValidators(BaseValidator):
    def validate(self):
        pass


class EmailHeadersGenerators:
    def __init__(self, recipient, task_id):
       self.recipient= recipient
       self.subject = self.generate_mail_body(recipient, task_id)
    
    def __repr__(self):
        return f"From: KEN LUMULI <{MAIN_SENDER_EMAIL}>\n"
                "To: <{self.recipient}> \n" 
                "Subject: {self.subject}\n"
                "Body: "


    def generate_mail_body(self, user: worker, task_id: int):

        """
        prepare Message for each specific task
        if the task has attachment then an email with attachment is sent
        """

        with DatabaseContextManager() as context_manager:
            task = context_manager.session.query(Task).filter(
                    task_id = task_id
            ).first()

            if task:
                if not task.has_attachment:
                    return f"""
                        Hello {user.name}, A task has been upload that may match your sklls
                        Feel free to handle the task
                    """
                else:
                    # use the filebaseclass to handle files
                    pass
            raise TaskNotFoundError

class Main(BaseNotifier):
    def __init__(self):
        """
        Send email messages to already subscribed users.
        """

        super(self, BaseNotifier).__init__(*args, **kwargs)
        self.headers = Parser(policy=default).parsestr(EmailHeadersGenerators(self.recepient))


    def parse(self):
        self.from_addr = self.headers['from']
        self.to_addr = self.headers['to']

    def send(self):
        with smtplib.SMTP('localhost') as server:
            server.send(self.headers)


    def send_mail_with_attchment(self):
        with smtplib.SMTP('localhost') as server:
            server.send(self.headers)

    def serve_forever(self):
        while True:
            self.send()

if __name__ == '__main__':
    server = Main()
    server.serve_forever()
