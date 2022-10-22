from __future__ import annotations
from email.message import EmailMessage
import mimetypes
from _base_notify import BaseNotifier
# from email.parser import Parser, BytesParser
# from email.policy import default
from logger import logger
import os
from collections.abc import MutableMapping
from abc import ABC, abstractmethod
from collections import UserList
import smtplib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from App.databasemanager import DatabaseContextManager
from App.models import User, Tasks
import app

# email_re = re.compile(r'([a-z]*)(\@gmail.com)')

MAIN_SENDER_EMAIL = "lumulikenreagan@gmail.com" # replace with environment Variable


class UserTask(MutableMapping):
    class SuggestionBase:
        def __init__(self, user, suggestion):
            self.user: User = user
            self.suggestion: Tasks = suggestion

    def __init__(self):
        self.suggestions = []
   
    def __getitem__(self, user):
        for details in self.suggestions:
            if user == details.user:
                return details.suggestion
            raise KeyError

    def __setitem__(self, user: User, suggestion: Task):
        for details in self.suggestions:
            if user == details.user:
                details.value = suggestion
                return
        self.suggestions.append(self.SuggestionBase(user, suggestion))

    def __delitem__(self, key):
        for idx in len(self):
            if key == self.suggestions[idx].user:
                self.suggestions.pop(key)
                return self
            raise KeyError

   
    def __repr__(self):
        return f"[{task for task in self.suggestions}]"

    def __iter__(self):
        for item in self.suggestions:
            yield item


    def __len__(self):
        return len(self.suggestions)

    def __le__(self, other: "UserTask")-> bool:
        if self.__class__ == other.__class__:
            return len(self) < len(other)
        raise NotImplementedError

    def __gt__(self, other: "UserTask") -> bool:
        if self.__class__ == other.__class__:
            return len(self) > len(other)
        raise NotImplementedError

    def __eq__(self, other: "UserTask") -> bool:
        if self.__class__ == other.__class__:
            return len(self) == len(other)
        raise NotImplementedError


class MailTaskSuggestor:
    def __init__(self, user_id):
        self.user = user_id
        self.mailed_tasks = UserTask()


    def generate_task(self) -> UserTask:
        with app.app.app_context():
            with DatabaseContextManager() as context_manager:
                task = context_manager.session.query(Tasks).all()
                user = context_manager.session.query(User).filter(
                    User.id == self.user        
                ).first()
            
                if user:
                    if task:
                        for tasks in task:
                            # if tasks.payment_status == "paid" and tasks.progress_status == "unclaimed":
                            self.mailed_tasks[user] = tasks
        return self.mailed_tasks


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


class MailBasket(UserList):
    pass


class EmailHeadersGenerators:
    def __init__(self):
        self.basket = MailBasket()

    def generate_headers(self) -> Iterable[EmailMessage]:
        self.suggestions: UserTask = MailTaskSuggestor(1).generate_task()
        for det in self.suggestions:
            message = EmailMessage()
            message['Subject'] = det.suggestion.title
            message['From'] = MAIN_SENDER_EMAIL
            message['To'] = det.user.email
            message.set_content(f"""
Hello {det.user.name} A task has been uploaded that meets your qualifications 
click the link below if you can handle it
http:://localhost:5000/worker/claim/task/{det.suggestion.id}
            """)
                ## Append the Message to the global EMailHandler
                ## Handle attachment incase required
            self.basket.append(message)
        return self.basket


class MailNotifier:
    pass


class MailHandler(BaseNotifier):
    def __init__(self) -> None:
        """
        Send email messages to already subscribed users.
        """
        self.messages = EmailHeadersGenerators().generate_headers()

    def send(self) -> None:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(MAIN_SENDER_EMAIL, os.environ.get('MAIL_PASSWORD'))
            for message in self.messages:
                server.send(message)
                self.messages.remove(message)
        server.quit()

    def send_mail_with_attchment(self) -> None:
        with smtplib.SMTP('localhost') as server:
            server.send(self.headers)

    def serve_forever(self) -> None:
        while len(self.messages) > 0:
            self.send()
        else:
            logger.warning("No messages in queue")
            return

if __name__ == '__main__':
    m = MailHandler()
    m.serve_forever()
