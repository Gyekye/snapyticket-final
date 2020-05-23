from django.shortcuts import redirect, render
from django.views.generic import View,UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from .decorators import EventOrganizerRequired
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Organizer
from django.contrib import messages
from django.urls import reverse_lazy

# view for displaying the dashboard to the organizer
class DashBoardView(LoginRequiredMixin,EventOrganizerRequired,View):
    def get(self, request, *args, **kwargs):
        return render(request,'organizer/dashboard.html')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')


# view for updating an organizers info
class OrganizerUpdate(LoginRequiredMixin,EventOrganizerRequired,UpdateView):
    model = Organizer
    fields = ['name','logo','email','twitter','instagram','facebook','telegram',]
    success_url = reverse_lazy('organizer:dashboard')
    template_name = 'organizer/update.html'
    
    # returns a valid form 
    def form_valid(self, form):
        """If the form is valid, save the associated model. and display a success message"""
        self.object = form.save()
        messages.info(self.request,"You have successfully updated your details")
        return super().form_valid(form)


