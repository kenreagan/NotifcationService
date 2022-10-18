from __future__ import annotations
from email.message import EmailMessage
import mimetypes
from _base_notify import BaseNotifier
from email.parser import Parser, BytesParser
from email.policy import default
from App.databasemanager import DatabaseContextManager
from App.models import User, Task
from logger import logger
import os
from collections.abc import MutableMapping
# email_re = re.compile(r'([a-z]*)(\@gmail.com)')

MAIN_SENDER_EMAIL = "lumulikenreagan@gmail.com" # replace with environment Variable


class UserTask(UserList):
    class SuggestionBase:
        def __init__(self, user, suggestion):
            self.user: User = user
            self.suggestion: Task = suggestion

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
        self.suggestions.append(user, suggestion)

    def __delitem__(self, key):
        for idx in len(self):
            if key == self.suggestions[idx].user:
                self.suggestions.pop(key)
                return self
            raise KeyError

   
    def __repr__(self):
        return f"[{task for task in user_tasks}]"

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
        mailed_tasks = UserTask()


    def generate_task(self):
        with DatabaseContextManager() as context_manager:
            task = context_manager.session.query(Task).all()
            user = context_manager.session.query(User).filter(
                user_id = user_id        
            ).first()
            
            if user:
                if task:
                    for tasks in task:
                        mailed_tasks[user] = tasks
        yield mailed_tasks


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
        return f"From: KEN LUMULI <{MAIN_SENDER_EMAIL}>\n To: <{self.recipient}>"
    
    def generate_mail_body(self):
        tasks = MailTaskSuggestor(recipient).generate_task()


class MailNotifier:
    pass


class MailHandler(BaseNotifier):
    def __init__(self):
        """
        Send email messages to already subscribed users.
        """

        super(self, BaseNotifier).__init__(*args, **kwargs)
        self.headers = Parser(policy=default).parsestr(EmailHeadersGenerators(self.recepient))
        print(dir(self.headers))


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
        logger.info("Preparing Server")
        while True:
            self.send()

if __name__ == '__main__':
    server = MailHandler()
    server.serve_forever()
