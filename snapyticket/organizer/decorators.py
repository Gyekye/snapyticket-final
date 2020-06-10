from django.contrib.auth.mixins import AccessMixin
from django.http.response import HttpResponse
from .models import Organizer
from django.db.models import ObjectDoesNotExist

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
        # checks whether user is organizer and has been approved
        try:
            _approved_status = Organizer.objects.get(user=request.user)
            if _approved_status.is_approved_status == False:
                # ! replace httpresponse with a template
                return HttpResponse("You are haave not been approved yet. Please go back")
        except (ObjectDoesNotExist,AttributeError):
            # ! replace Httpresponse with template
            return HttpResponse('You are not an organizer, Kindly go back home')
        return super().dispatch(request, *args, **kwargs)


class VerifiedOrganizerRequired(AccessMixin):
    """Verify that the current  organizer is verified ."""
    def dispatch(self, request, *args, **kwargs):
        # gets the verified status of the organizer
        try:
            _status = Organizer.objects.get(user=request.user)
            # if its false returns an http response
            if _status.is_verified_status == False:
                # ! replace httptresponse with template
                return HttpResponse("Verfied Organizers Only")
        except ObjectDoesNotExist:
            return HttpResponse('Go back Home')
        return super().dispatch(request, *args, **kwargs)
