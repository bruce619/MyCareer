from django import template

from nueoffshore.models import Applicants
from django.contrib.auth.models import Group

register = template.Library()


@register.simple_tag(name='is_already_applied')
def is_already_applied(job, user):
    applied = Applicants.objects.filter(job=job, user=user)
    if applied:
        return True
    else:
        return False


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


