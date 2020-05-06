from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.http import HttpResponse
from .models import Ticket,TicketItem,TicketBag
from .forms import AddToCartForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
class TicketView(TemplateView):
    template_name = 'ticket/tickets.html'
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.all()
        return self.render_to_response(context)
    
class TicketDetail(DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name='ticket/details.html'


def _add_to_cart(request,slug):
    # gets the ticket with a specific slug
    _ticket = Ticket.objects.get(slug=slug)
    if request.method == 'POST':
        # gets the ticket_type from the form
        _type = request.POST.get('ticket_type')
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # gets the ticket varaition of a specific ticket 
            _ticket_type = _ticket.ticketvariation_set.get(variation=_type,ticket=_ticket)
            #  gets the cleaned data from the form
            _quantity = form.cleaned_data.get('quantity')
            form.save(commit=False)
            try:
                # try to check if the ticket item exits already an if it does will update the quantity
                _existing_ticket_item = TicketItem.objects.get(user=request.user,ticket=_ticket,ticket_type=_ticket_type)
                # increases the quantity of the order item by the quantity typed
                _existing_ticket_item.quantity += _quantity
                _existing_ticket_item.save()
                return HttpResponse('updated quantity')
            # else creates a new ticket item and saves it 
            except:
                # creates a new ticket item
                ticket_item,created = TicketItem.objects.get_or_create(
                    user=request.user,
                    ticket = _ticket,
                    quantity = _quantity,
                    ordered = False,
                    ticket_type = _ticket_type
                )# saves new ticket_item 
                ticket_item.save()
                # creates or gets a ticket bag
                new_ticket_bag,created = TicketBag.objects.get_or_create(
                    user=request.user,
                )
                # saves ticket bag
                new_ticket_bag.save()
                # addeds newly created ticket to the ticket bag
                new_ticket_bag.tickets.add(ticket_item)
                #print(new_ticket_bag.tickets.quantity)
                return HttpResponse("added to cart")
    else:
        form = AddToCartForm()
    context = {'ticket':_ticket,'form':form}
    return render(request,'ticket/bag.html',context)
