from django.shortcuts import redirect, render
from django.views.generic import TemplateView,UpdateView,View
from django.http import HttpResponse, HttpResponseRedirect
from .decorators import EventOrganizerRequired,VerifiedOrganizerRequired
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Organizer
from ticket.models import Ticket, TicketItem
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import OrganizerRegisterForm
from django.db.models import ObjectDoesNotExist
from django.db import IntegrityError

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


class RegisterOrganizerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        form = OrganizerRegisterForm()
        context = {'form':form}
        
        return render(request,'organizer/register.html',context)

    def post(self, request, *args, **kwargs):
        
        form = OrganizerRegisterForm(request.POST,request.FILES)
        
        if form.is_valid():
            #? org is the short form of organizer
            #? gets the clean data from model form for custom validation
            # #* Core credentials 
            org_name = form.cleaned_data.get('name')
            org_email = form.cleaned_data.get('email')
            org_logo  = form.cleaned_data.get('logo')
            
            #* Social Media Accounts
            org_instagram = form.cleaned_data.get('instagram')
            org_facebook  = form.cleaned_data.get('facebook')
            org_telegram  = form.cleaned_data.get('telegram')
            
            #! Custom Validations for cleaned data from forms
            if len(org_name) > 100:
                messages.info(request,'name should be at least 100')
                return redirect('organizer:register')
            if Organizer.objects.filter(name=org_name).exists():
                return HttpResponse('name is taken')
            if Organizer.objects.filter(email=org_email).exists():
                return HttpResponse('Email is taken')
            try:
                        
                new_organizer = Organizer.objects.create(
                    user=request.user,
                    name=org_name,
                    email=org_email,
                    logo=org_logo,
                    instagram=org_instagram,
                    facebook=org_facebook,
                    telegram=org_telegram
                )
                #* create a new organizer instance 
                new_organizer.save()
                messages.info(request,'registered wait for approval')
                return redirect('profile:user_profile')
                
            except IntegrityError:
                return HttpResponse('Already registered ')
        else:
            form = OrganizerRegisterForm()
        context = {'form':form}
        return render(request,'organizer/register.html',context)

class OrganizerEventsView(EventOrganizerRequired, View):
    def get(self, *args, **kwargs):
        events = Ticket.objects.filter(organizer=self.request.user.organizer)
        context = {'events': events}
        return render(self.request, 'organizer/events.html', context)


def track_event(request, slug):
    event = Ticket.objects.get(slug=slug)
    sales = TicketItem.objects.filter(ticket=event, ordered=True)
    context = {'event': event, 'sales': sales}
    return render(request, "organizer/track.html", context)


def event_sales(request, slug):
    e = Ticket.objects.get(slug=slug)
    sales = TicketItem.objects.filter(ticket=e)
    context = {'sales': sales}
    return render(request, 'organizer/sales.html', context)