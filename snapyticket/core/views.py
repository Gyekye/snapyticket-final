import random
import string
from PIL import Image
from django.shortcuts import redirect, render
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticket.models import TicketBag,TicketItem
from django.conf import settings

# Create your views here.
def create_ref_code():
    # Generates a reference codes for order
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class IndexView(TemplateView):
    template_name = 'core/index.html'
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:home')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
 
 
class PaymentView(LoginRequiredMixin,TemplateView):
    template_name = 'core/payment.html'
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['pubkey'] = settings.RAVE_PUBLIC_KEY
        context['currency'] =  settings.RAVE_CURRENCY
        context['user_order'] = TicketBag.objects.get(user=request.user,ordered=False)
        return self.render_to_response(context)
    

class SuccessView(LoginRequiredMixin,TemplateView):
    template_name = 'redirects/payment/success.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # gets the ticket bag of the user that has paid 
        user_ticket_bag = TicketBag.objects.get(user=request.user,ordered=False)
        user_ticket_item_unpaid = TicketItem.objects.filter(user=request.user, ordered=False)
        # saves the ticket bag order  to true 
        user_ticket_bag.ordered = True
        # checks if ticket bag is ordered
        if user_ticket_bag.ordered == True:
            # gets all the tickets in the ticket bag
            for ticketitems in user_ticket_bag.tickets.all():
                # sets the ticket item ordered to true
                ticketitems.ordered = True
                ticketitems.ticket_code = create_ref_code()
                # saves the ticket item order 
                ticketitems.save()
        # saves ticket bag after setting ordered equals True
        user_ticket_bag.save()
        # pass the context to the template
        context['ordered_ticket'] = user_ticket_bag
        return self.render_to_response(context)


class FailedView(LoginRequiredMixin,TemplateView):  
    template_name = 'redirects/payment/failed.html'
 
    
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
