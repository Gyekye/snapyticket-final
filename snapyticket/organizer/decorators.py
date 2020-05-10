from django.contrib.auth.mixins import AccessMixin
from django.http.response import HttpResponse


# Function based decorator
def organizer_only(view_func):
    """ Verify if the user is an organizer"""
    def wrap(request,*args, **kwargs):
        if request.user.is_organizer:
            return view_func(request,*args, **kwargs)
        return HttpResponse("You are not allowed here")
    return wrap


# class based decorators called Mixin
class EventOrganizerRequired(AccessMixin):
    """Verify that the current user is organizer."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer:
            return HttpResponse("You are not allowed here Kindly go back")
        return super().dispatch(request, *args, **kwargs)
