FROM python::latest

WORKDIR /Notification

COPY . /Notifications

RUN cd Notifications/

RUN python _mail_handler.py
