from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


# Function based decorator
def organizer_only(view_func):
    """ Verify if the user is an organizer"""
    def wrap(request,*args, **kwargs):
        if request.user.is_organizer:
            return view_func(request,*args, **kwargs)
        return HttpResponse("You are not allowed here")
    return wrap


# class based decorators called Mixi
class EventOrganizerRequired(AccessMixin):
    """Verify that the current user is organizer."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer:
            messages.info(request,'You are not an event organizer.')
            return redirect('profile:user_profile')
        return super().dispatch(request, *args, **kwargs)

