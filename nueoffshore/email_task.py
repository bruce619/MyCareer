import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class EmailThreadOne(threading.Thread):
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


def send_html_mail(subject, sender, recipient_list, context, html_content):
    EmailThreadOne(subject, sender, recipient_list, context, html_content).start()