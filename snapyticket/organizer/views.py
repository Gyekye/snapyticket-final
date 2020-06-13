from django.shortcuts import redirect, render
from django.views.generic import TemplateView,UpdateView,View
from django.http import HttpResponse, HttpResponseRedirect
from .decorators import EventOrganizerRequired,VerifiedOrganizerRequired
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Organizer
from ticket.models import Ticket, TicketItem,TicketBag
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import OrganizerRegisterForm
from django.db.models import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
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
                send_mail(
                        'Organizer Registration Email',
                        f'''Thank You for requesting to become an organizer to share content on this beautiful platform.We will send you another email to confirm your registration.Thank You {request.user.username}''',
                        settings.EMAIL_HOST_USER,
                        [new_organizer.email],
                        fail_silently=False,
                        )
                messages.info(request,'registered wait for approval email')
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




class EventSales(TemplateView):
    template_name = 'organizer/sales.html'
    
    # renders dynamic data to the home page
    def get(self,request,slug,*args,**kwargs):
        event_ticket = Ticket.objects.get(slug=slug,organizer=self.request.user.organizer)
        context = self.get_context_data(**kwargs)

        #* generate the total ticket sales revenue
        total_revenue = 0
        for ordered_ticket_revenue in TicketItem.objects.filter(
            ticket__organizer=self.request.user.organizer,ticket=event_ticket):
            total_revenue += ordered_ticket_revenue.ticket_item_price()
        #* end
        #? call total_revenue in the html to get the total revenue of an organizer
        
        context['total_revenue'] = total_revenue
        context['sales'] = TicketItem.objects.filter(ticket=event_ticket,ordered=True)
        context['event'] = event_ticket
        return self.render_to_response(context)
        

class TrackEventSales(TemplateView):
    template_name = 'organizer/track.html'
    
    # renders dynamic data to the home page
    def get(self,request,slug,*args,**kwargs):
        event_ticket = Ticket.objects.get(slug=slug,organizer=self.request.user.organizer)
        context = self.get_context_data(**kwargs)
        #* generate the total ticket sales revenue
        total_revenue = 0
        for ordered_ticket_revenue in TicketItem.objects.filter(
            ticket__organizer=self.request.user.organizer,ticket=event_ticket):
            total_revenue += ordered_ticket_revenue.ticket_item_price()
        #* end
        #? call total_revenue in the html to get the total revenue of an organizer
        
        context['sales'] = TicketItem.objects.filter(ticket=event_ticket,ordered=True).order_by('-ordered_on')
        context['graph_sales'] = TicketItem.objects.filter(ticket=event_ticket,ordered=True)
        context['total_revenue'] = total_revenue
        context['event'] = event_ticket
        return self.render_to_response(context)

class RequestPaymentView(TemplateView):
    template_name = 'organizer/request-payment.html'

    # renders dynamic data to the home page
    def get(self,request,slug,*args,**kwargs):
        event_ticket = Ticket.objects.get(slug=slug,organizer=self.request.user.organizer)
        context = self.get_context_data(**kwargs)
        #* generate the total ticket sales revenue
        total_revenue = 0
        for ordered_ticket_revenue in TicketItem.objects.filter(
            ticket__organizer=self.request.user.organizer,ticket=event_ticket):
            total_revenue += ordered_ticket_revenue.ticket_item_price()
        #* end
        
        context['total_revenue'] = total_revenue
        context['event'] = event_ticket
        return self.render_to_response(context)