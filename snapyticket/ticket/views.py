from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView,View

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


class UpdateTicketItem(UpdateView):
    model = TicketItem
    fields = ['quantity']
    success_url = reverse_lazy('ticket:ticket_bag_summary')
    template_name = 'ticket/update_ticket_item.html'

    def form_valid(self, form):
        """ Checks for the validity of the data being passed into the form"""
        _ticket_item_quantity = form.cleaned_data.get('quantity')
        # Return an httpResponse when the quantity falls below onw
        if _ticket_item_quantity < 1:
            return  HttpResponse("Quantity must not go below one")
        else:
            # if quantity is greater than or equals one then call save method
            form.save()
        return super().form_valid(form)


class PaymentView(View):
    pass


@login_required
def _add_to_cart(request, slug):
    # gets the ticket with a specific slug
    _ticket = Ticket.objects.get(slug=slug)
    #print(_ticket.ticketitem_set.all())
    if request.method == 'POST':
        # gets the ticket_type from the form
        _type = request.POST.get('ticket_type')
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # gets the ticket variation of a specific ticket
            _ticket_type = _ticket.ticketvariation_set.get(variation=_type, ticket=_ticket)
            #  gets the cleaned data from the form
            _quantity = form.cleaned_data.get('quantity')
            form.save(commit=False)
            try:
                # try to check if the ticket item exits already an if it does will update the quantity
                _existing_ticket_item = TicketItem.objects.get(user=request.user, ticket=_ticket,
                                                               ticket_type=_ticket_type)
                # increases the quantity of the order item by the quantity typed
                _existing_ticket_item.quantity += _quantity
                _existing_ticket_item.save()
                return HttpResponse('updated quantity')
            # else creates a new ticket item and saves it 
            except:
                # creates a new ticket item
                _ticket_item, created = TicketItem.objects.get_or_create(
                    user=request.user,
                    ticket=_ticket,
                    quantity=_quantity,
                    ordered=False,
                    ticket_type=_ticket_type
                )  # saves new ticket_item
                # checks to see the quantity entered does not fall below one
                if _ticket_item.quantity < 1:
                    # if it falls below one, then update to 1 then save
                    _ticket_item.quantity = 1
                    _ticket_item.save()
                else:
                    _ticket_item.save()
                # creates or gets a ticket bag
                _new_ticket_bag, created = TicketBag.objects.get_or_create(
                    user=request.user,
                )
                # saves ticket bag
                _new_ticket_bag.save()
                # added newly created ticket to the ticket bag
                _new_ticket_bag.tickets.add(_ticket_item)
                # print(new_ticket_bag.tickets.quantity)
                return HttpResponse("added to cart")
    else:
        form = AddToCartForm()
    context = {'ticket': _ticket, 'form': form}
    return render(request, 'ticket/bag.html', context)


@login_required
def _remove_from_cart(request, slug, pk):
    # todo build a functionality to decrease the number of ticket items by 1 the remove when its zero
    # gets the specific ticket to remove from ticket bag
    _ticket_to_remove = get_object_or_404(TicketItem, user=request.user, slug=slug, id=pk)
    # gets users ticket bag
    _ticket_bag = TicketBag.objects.get(user=request.user, ordered=False)
    # removes ticket item from users ticket bag
    _ticket_bag.tickets.remove(_ticket_to_remove)
    # then deletes other if all ticket items are gone
    TicketItem.delete(_ticket_to_remove)
    #  deletes the users ticket bag when there are no tickets in them
    if _ticket_bag.tickets.count() == 0:
        TicketBag.delete(_ticket_bag)
    # todo create a redirect to ticket bag
    return HttpResponse('Item removed from ticket items')


def _ticket_bag_summary(request):
    _user_ticket_bag = get_object_or_404(TicketBag, user=request.user)
    context = {'ticket_bag': _user_ticket_bag}
    return render(request, 'ticket/ticket_bag_summary.html', context)
