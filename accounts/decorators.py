from django.core.exceptions import PermissionDenied


def user_is_human_resources(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_human_resources:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def user_is_applicant(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_applicant:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_superuser(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
