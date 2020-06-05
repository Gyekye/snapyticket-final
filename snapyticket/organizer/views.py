from django.shortcuts import redirect, render
from django.views.generic import TemplateView,UpdateView,CreateView
from django.http import HttpResponse, HttpResponseRedirect
from .decorators import EventOrganizerRequired,VerifiedOrganizerRequired
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Organizer
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import OrganizerRegisterForm

# view for displaying the dashboard to the organizer
class DashBoardView(EventOrganizerRequired,LoginRequiredMixin,TemplateView):
    template_name = 'organizer/dashboard.html'
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
 
 
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


class RegisterOrganizer(LoginRequiredMixin,CreateView):
    form_class = OrganizerRegisterForm
    template_name = 'organizer/register.html'
    success_url  = reverse_lazy('organizer:dashboard')
    