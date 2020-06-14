import json
#import unirest
import requests
#unirest is a http library. You can use any http library you prefer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, DetailView, UpdateView, View
from .forms import AddToCartForm
from .models import Ticket, TicketItem, TicketBag,SavedTicket
from django.db.models import ObjectDoesNotExist


# Search
@login_required
def tickets(request):
    query = request.GET.get('query')
    tickets = Ticket.objects.all()
    if query == None:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(title__icontains=query)
    
    context = {'tickets': tickets, 'search': query}
    return render(request, 'ticket/tickets.html', context)


class TicketDetail( LoginRequiredMixin, DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'ticket/details.html'

class SavedTickets(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        saved_tickets = SavedTicket.objects.filter(user=self.request.user, is_saved=True)
        context = {'saved_tickets':saved_tickets}
        return render(self.request, 'ticket/saved.html', context)

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
                existing_ticket_bag = TicketBag.objects.filter(
                    user=request.user,
                    ordered=False
                )[0]
                existing_ticket_item = TicketItem.objects.get(
                    user=request.user, 
                    ticket=ticket,
                    ticket_type=ticket_type,
                    ordered=False
                    )
                if existing_ticket_item in existing_ticket_bag.tickets.all():
                    # increases the quantity of the order item by the quantity typed
                    existing_ticket_item.quantity += quantity
                    existing_ticket_item.save()
                    messages.success(request,"Updated Quantity")
                    return redirect('ticket:ticket_bag_summary')
                
            # ! This expect block handles the two errors thrown from the try block above
            # ! Without it the except part of the code would not be exceuted
            except(IndexError,ObjectDoesNotExist): 
                # else creates a new ticket item and saves it 
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
                    messages.success(request, "Added ticket to your bag sucessfully")
                    return redirect('ticket:ticket_bag_summary')
                else:
                    messages.error(request, 'No ticket bag was found')
                    return redirect(request, f"/ticket/{slug}/add_to_cart")
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
        messages.success(request, "You do not have any active Order")
        return redirect("ticket:tickets")
    messages.success(request, "Removed ticket from your bag sucessfully")
    return redirect("ticket:ticket_bag_summary")


@login_required
def ticket_bag_summary(request):
    try:
        user_ticket_bag = TicketBag.objects.filter(
            user=request.user,
            ordered=False,
            tickets__ordered=False
            )[0]
    except:
        messages.warning(request, "You do not have any Active Order")
        return redirect(f'/ticket/')
    context = {'ticket_bag': user_ticket_bag}
    return render(request, 'ticket/ticket_bag_summary.html', context)

@login_required
def add_to_saved(request,slug):
    # gets a ticket with the slug
    ticket_to_save = Ticket.objects.get(slug=slug)
    try:
        # check for already saved ticket 
        previous_saved_ticket = SavedTicket.objects.get(user=request.user,is_saved=True)
        # if ticket in saved tickets 
        if ticket_to_save in previous_saved_ticket.ticket.all():
            # remove ticket from saved 
            previous_saved_ticket.ticket.remove(ticket_to_save)
            messages.success(request, "Removed From Saved Tickets")
            return redirect('ticket:saved')
        else:
            # add to saved tickets
            previous_saved_ticket.ticket.add(ticket_to_save)
            previous_saved_ticket.save()
            messages.success(request, "Added To Saved Tickets")
            return redirect('ticket:saved')
    # create a new saved ticket queryset if some doesnt exist
    except (ObjectDoesNotExist,TypeError):
        new_saved_ticket_bag = SavedTicket.objects.create(user=request.user,is_saved=True)
        new_saved_ticket_bag.save()
        new_saved_ticket_bag.ticket.add(ticket_to_save)
        new_saved_ticket_bag.save()
        messages.success(request, "Added To Saved Tickets")
        return redirect('ticket:saved')


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
