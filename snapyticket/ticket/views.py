import json
#import unirest
import requests
#unirest is a http library. You can use any http library you prefer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, DetailView, UpdateView, View

from .forms import AddToCartForm
from .models import Ticket, TicketItem, TicketBag


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
    template_name = 'ticket/details.html'

# todo replace httpResponse redirects with messages
class UpdateTicketItem(UpdateView):
    model = TicketItem
    fields = ['quantity']
    success_url = reverse_lazy('ticket:ticket_bag_summary')
    template_name = 'ticket/update_ticket_item.html'

    def form_valid(self, form):
        """ Checks for the validity of the data being passed into the form"""
        ticket_item_quantity = form.cleaned_data.get('quantity')
        # Return an httpResponse when the quantity falls below onw
        if ticket_item_quantity < 1:
            return HttpResponse("Quantity must not go below one")
        else:
            # if quantity is greater than or equals one then call save method
            form.save()
        return super().form_valid(form)


@login_required
def add_to_cart(request, slug):
    # gets the ticket with a specific slug
    ticket = Ticket.objects.get(slug=slug)
    # print(_ticket.ticketitem_set.all())
    if request.method == 'POST':
        # gets the ticket_type from the form
        t_type = request.POST.get('ticket_type')
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # gets the ticket variation of a specific ticket
            ticket_type = ticket.ticketvariation_set.get(
                variation=t_type, 
                ticket=ticket
                )
            #  gets the cleaned data from the form
            quantity = form.cleaned_data.get('quantity')
            form.save(commit=False)
            try:
                existing_ticket_item = TicketItem.objects.get(
                    user=request.user, 
                    ticket=ticket,
                    ticket_type=ticket_type,
                    ordered=False
                    )
                if existing_ticket_item.exists():
                    # increases the quantity of the order item by the quantity typed
                    existing_ticket_item.quantity += quantity
                    existing_ticket_item.save()
                    return HttpResponse('updated quantity')
            # else creates a new ticket item and saves it 
            except:
                # creates or gets a ticket bag
                new_ticket_bag, created = TicketBag.objects.get_or_create(
                    user=request.user,
                    ordered=False,
                    tickets__ordered=False,
                    tickets__ticket_type = ticket_type
                )
                # saves ticket bag
                new_ticket_bag.save()
                ticket_bag_query = TicketBag.objects.filter(user=request.user,ordered=False)
                ticket_bag_query = ticket_bag_query[0]
                if ticket_bag_query:
                    # creates a new ticket item
                    ticket_item = TicketItem.objects.create(
                        user=request.user,
                        ticket=ticket,
                        quantity=quantity,
                        ordered=False,
                        ticket_type=ticket_type
                    )  # saves new ticket_item
                    
                    # added newly created ticket to the ticket bag
                    ticket_bag_query.tickets.add(ticket_item)
                    # print(new_ticket_bag.tickets.quantity)
                    ticket_bag_query.save()
                    ticket_bag_to_remove = TicketBag.objects.filter(user=request.user,ordered=False)
                    print(ticket_bag_to_remove)
                    return HttpResponse("added to cart")
                else:
                    return HttpResponse('No ticket bag ')
    else:
        form = AddToCartForm()
    context = {'ticket': ticket, 'form': form}
    return render(request, 'ticket/bag.html', context)


@login_required
def remove_from_cart(request, slug, pk):
    # todo build a functionality to decrease the number of ticket items by 1 the remove when its zero
    # gets the specific ticket to remove from ticket bag
    ticket_to_remove = get_object_or_404(TicketItem, 
                                         user=request.user, 
                                         slug=slug, 
                                         id=pk, 
                                         ordered=False
                                         )
    # gets users ticket bag
    ticket_bag = TicketBag.objects.filter(
        user=request.user, 
        ordered=False, 
        tickets__ordered=False
        )[0]
    # removes ticket item from users ticket bag
    ticket_bag.tickets.remove(ticket_to_remove)
    # then deletes other if all ticket items are gone
    TicketItem.delete(ticket_to_remove)
    #  deletes the users ticket bag when there are no tickets in them
    if ticket_bag.tickets.count() == 0:
        TicketBag.delete(ticket_bag)
    # todo create a redirect to ticket bag
    return HttpResponse('Item removed from ticket items')

@login_required
def ticket_bag_summary(request):
    user_ticket_bag = TicketBag.objects.filter(
        user=request.user,
        ordered=False,
        tickets__ordered=False
        )[0]
    context = {'ticket_bag': user_ticket_bag}
    return render(request, 'ticket/ticket_bag_summary.html', context)


#todo fix the webhooks and do a proper server side validation
#@require_POST
#@csrf_exempt
#def _receive_payment(request):
#    data = json.loads(request.body)
#    print(data)
#    return HttpResponse(status=200)


#def _confirm_payment(responds):
#  data = responds.body
#   print(data)
#   return  HttpResponse(status=200)
