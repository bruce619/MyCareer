import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from .models import Job
from django.utils import timezone


class EmailThread(threading.Thread):
    def __init__(self, subject, sender, recipient_list, context, html_content):
        self.subject = subject
        self.context = context
        self.sender = sender
        self.html_content = str(html_content)
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(subject=self.subject, from_email=self.sender, to=[self.recipient_list])
        html_template = get_template(self.html_content).render(self.context)
        msg.attach_alternative(html_template, "text/html")
        msg.send()


# @background(schedule=60)
def send_html_mail(subject, sender, recipient_list, context, html_content):
    EmailThread(subject, sender, recipient_list, context, html_content).start()


class EmailThreadTwo(threading.Thread):
    def __init__(self, subject, sender, recipient_list, context, html_content):
        self.subject = subject
        self.context = context
        self.html_content = str(html_content)
        self.sender = sender
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(subject=self.subject, from_email=self.sender, to=[self.recipient_list])
        html_template = get_template(self.html_content).render(self.context)
        msg.attach_alternative(html_template, "text/html")
        msg.send()


def send_html_mail_message(subject, sender, recipient_list, context, html_content):
    EmailThreadTwo(subject, sender, recipient_list, context, html_content).start()


# def auto_mark_as_filled(current_date):
#     jobs = Job.objects.all()
#     for job in jobs:
#         if current_date >= job.end_date:
#             job.filled = True
#             job.save()
#
#
# current_date = timezone.now()
#
# auto_mark_as_filled(current_date)

