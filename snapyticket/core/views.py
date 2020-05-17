import random
import string
import qrcode 
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
        # saves the ticket bag order  to true 
        user_ticket_bag.ordered = True
        # checks if ticket bag is ordered
        if user_ticket_bag.ordered == True:
            # gets all the tickets in the ticket bag
            for ticketitems in user_ticket_bag.tickets.all():
                # sets the ticket item ordered to true
                ticketitems.ordered = True
                # saves the ticket item order 
                ticketitems.save()
            # creates a special sequence of strings for the ticket bag which has been ordered as the order id 
            user_ticket_bag.order_ref_code = create_ref_code()
            # saves the ticket bag after giving it a order ID
            user_ticket_bag.save()
            # loops through the ticksts in the  ticket bag 
            for ticket_item in user_ticket_bag.tickets.all():
                # sets a counter to zero
                counter = 0
                # while the counter is less than the number of tickets in the ticket bag
                # keep making more qrcodes for each ticket item
                # so each ticket item will have its own qrcode which will be saved to its model 
                # this image can be accessed with the {{TicketItem.qr_image.url}} in the templates
                while counter < ticket_item.quantity:
                    # while the counter is less than the ticketItem quantity keep making qrcodes
                    # increase counter by one
                    counter = counter + 1
                    ticket_item_qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                    )
                    ticket_item_qr.add_data(
                        # the qrcode for each tickets consists of unique data
                        # its consists of the ticket_type
                        # its consist of the username of the user
                        # the order ref code 
                        # and the name of the ticket
                        # todo pass more data to the data in the qrcode 
                        f'PURCHASED BY: {self.request.user}\nVARAIATION: {ticket_item.ticket_type.variation}\nORDER ID: {user_ticket_bag.order_ref_code}',
                    )
                    ticket_item_qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    # saves the qrcode image to the media folder in the project directory in a folder called qr_codes
                    # todo fix the duplicatrion of the images upon saving 
                    ticket_item_qr.save(settings.MEDIA_ROOT +f'/qr_codes/{request.user}{ticket_item}{ticket_item.id}{counter}.png')
                    # creates the qr_image instance by opening it
                    open_image = Image.open(settings.MEDIA_ROOT +f'/qr_codes/{request.user}{ticket_item}{ticket_item.id}{counter}.png')
                    # saves the image
                    # todo make sure that the qrcode is indeed saved to the qr-image model of each ticket item
                    new_image = ticket_item.qr_image.save(open_image)
                    print(ticket_item.qr_image)
                    # break when counter is equal to the quantity of the ticket Item 
                    if counter == ticket_item.quantity:
                        break
        # saves ticket bag after setting ordered equals True
        user_ticket_bag.save()
        # pass the context to the template
        context['ordered_ticket'] = user_ticket_bag
        return self.render_to_response(context)

class FailedView(TemplateView):  
    template_name = 'redirects/payment/failed.html'
 
    
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
