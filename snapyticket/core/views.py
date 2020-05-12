from django.shortcuts import redirect, render
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticket.models import TicketBag,TicketItem
from django.conf import settings

# Create your views here.

class IndexView(TemplateView):
    template_name = 'core/index.html'

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


class SuccessView(TemplateView):
    template_name = 'redirects/payment/success.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # gets the ticket bag of the user that has paid 
        user_ticket_bag = TicketBag.objects.get(user=request.user,ordered=False)
        user_ticket_item_unpaid = TicketItem.objects.filter(user=request.user, ordered=False)
        # saves the order to true 
        user_ticket_bag.ordered = True
        if user_ticket_bag.ordered == True:
            for ticket_item in user_ticket_bag.tickets.all():
                ticket_item.ordered = True
                ticket_item.save()
        user_ticket_bag.save()
        return self.render_to_response(context)

class FailedView(TemplateView):  
    template_name = 'redirects/payment/failed.html'
 
    
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
