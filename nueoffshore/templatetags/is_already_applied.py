from django import template
from nueoffshore.models import Applicants, Notification, MessageStatus
from django.db.models import Count


register = template.Library()


@register.simple_tag(name='is_already_applied')
def is_already_applied(job, user):
    applied = Applicants.objects.filter(job=job, user=user)
    if applied:
        return True
    else:
        return False


@register.filter
def unread_notification(user):
    qs = Notification.objects.filter(receiver=user, messagestatus=MessageStatus.objects.get(name='message sent')).annotate(num_user=Count('sender')).count()
    return qs