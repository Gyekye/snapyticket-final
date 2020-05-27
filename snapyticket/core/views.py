import qrcode
import random
import string
from PIL import Image
from django.shortcuts import redirect, render
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticket.models import TicketBag,TicketItem,Ticket
from django.conf import settings
import base64

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
        context['user_order'] = TicketBag.objects.filter(user=request.user,ordered=False)[0]
        
        return self.render_to_response(context)
    
    
    
    
    
    
# payment success View 
class SuccessView(LoginRequiredMixin,TemplateView):
    template_name = 'redirects/payment/success.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # gets the ticket bag of the user that has paid 
        user_ticket_bag = TicketBag.objects.filter(user=request.user,ordered=False)[0]
        user_ticket_item_unpaid = TicketItem.objects.filter(user=request.user, ordered=False)
        
        # saves the ticket bag order  to true 
        user_ticket_bag.ordered = True
        
        # checks if ticket bag is ordered
        if user_ticket_bag.ordered == True:
            user_ticket_bag.order_ref_code = create_ref_code()
            # gets all the tickets in the ticket bag
            counter = 0
            for ticketitems in user_ticket_bag.tickets.all():
                # sets the ticket item ordered to true
                ticketitems.ordered = True
                ticketitems.ticket_code = create_ref_code()
                # saves the ticket item order 
                ticketitems.save()
                # Qr code generation logic below
                while counter < ticketitems.quantity:
                    counter = counter + 1
                    # main logic here 
                    ticket_item_qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=5,
                            border=4,
                    )
                    ticket_item_qr.add_data(
                        # the qrcode for each tickets consists of unique data
                        # its consists of the ticket_type
                        # its consist of the username of the user
                        # the order ref code 
                        # and the name of the ticket
                        # todo pass more data to the data in the qrcode 
                        f'''
                        PURCHASED BY: *************************{self.request.user}\n*******\n
                        VARAIATION: ***************************{ticketitems.ticket_type.variation}\n*******\n
                        ORDER ID: *************{user_ticket_bag.order_ref_code}\n*******\n
                        TICKET_CODE: *************{ticketitems.ticket_code}\n*******\n
                        ''',
                    )
                    # makes the size of the image fit
                    ticket_item_qr.make(fit=True)
                    # generates white and black qr code
                    img = ticket_item_qr.make_image(fill_color="black", back_color="white")
                    # saves the qrcode image to the media folder in the project directory in a folder called qr_codes
                    img.save(settings.MEDIA_ROOT+f'/qr_codes/{request.user}{counter}{ticketitems.ticket_code}.png')
                    # image generation termination logic begins 
                    # creates an object for the ticket qr model class ( foreign key to ticket item)
                    ticket_image = ticketitems.ticketitemqrimage_set.create(ticket_item=ticketitems)
                    # opens the image and encodes it to the bytes
                    with open(settings.MEDIA_ROOT+f'/qr_codes/{request.user}{counter}{ticketitems.ticket_code}.png', "rb") as imageFile:
                       str = base64.b64encode(imageFile.read())
                       # saves the image to the ticket_item_item_qr attribute
                       ticket_image.ticket_item_qr_image.save(f'{request.user}{ticketitems.ticket_code}{counter}.png',imageFile,save=True)
                       # saves the image to the model
                    ticketitems.save()
                    if counter == ticketitems.quantity and ticketitems.ticketitemqrimage_set.count() == ticketitems.quantity:
                        break
                # making the qrcode for other ticket Items 
                #todo add data to the qr data method 
                ticket_item_img = qrcode.make('Some data here')
                # condition to stop making qr code
                while ticketitems.ticketitemqrimage_set.count() < ticketitems.quantity:
                    # saves the image to the root media folder
                    ticket_item_img.save(settings.MEDIA_ROOT+f'/qr_codes/{request.user}{ticketitems.ticket_code}.png')
                    # open saved image
                    with open(settings.MEDIA_ROOT+f'/qr_codes/{request.user}{ticketitems.ticket_code}.png','rb') as ticket_qr:
                        # endcodes it
                        str = base64.b64encode(ticket_qr.read())
                        # creates a ticket item qr image instance 
                        ticket_img_qr_main = ticketitems.ticketitemqrimage_set.create(ticket_item=ticketitems)
                        # saves the qr image to the ticket item
                        ticket_img_qr_main.ticket_item_qr_image.save(f'{request.user}{ticketitems.ticket_code}.png',ticket_qr,save=True)
                        # saves the ticket
                        ticketitems.save()
                        #if ticketitems.ticketitemqrimage_set.count() == ticketitems.quantity:
                            #break
                    
        # saves ticket bag after setting ordered equals True 
        user_ticket_bag.save()
        # pass the context to the template
        context['ordered_ticket'] = user_ticket_bag
        return self.render_to_response(context)
    
# payment failure view 
class FailedView(LoginRequiredMixin,TemplateView):  
    template_name = 'redirects/payment/failed.html'
 
 
 
# Home View
class HomeView(LoginRequiredMixin, TemplateView):
    
    template_name = 'core/home.html'
    
    # renders dynamic data to the home page
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['all_tickets'] = Ticket.objects.all()
        return self.render_to_response(context)
