from django.urls import path
from .views import TicketDetail, tickets, add_to_cart, remove_from_cart, UpdateTicketItem, ticket_bag_summary,add_to_saved

app_name = 'ticket'

urlpatterns = [
    
    #* url pattern to see all approved tickets
    path('', tickets, name='tickets'),
    
    #* url pattern to see a ticket detail
    path('detail/<slug:slug>/', TicketDetail.as_view(), name='detail'),
    
    #* url pattern to add a ticket to a ticket bag
    path('<slug:slug>/add_to_cart/', add_to_cart, name='add_to_cart'),
    
    #* url pattern to add a ticket to saved ticket
    path('<slug:slug>/add_to_saved/',add_to_saved,name='add_to_saved'),
    
    #* url to remove a ticket from a ticket bag
    path('<slug:slug>/<int:pk>/remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    
    #* url to update a ticket item in a ticket bag
    path('<slug:slug>/<int:pk>/update_ticket_item/', UpdateTicketItem.as_view(), name='update_ticket_item'),
    
    #* url pattern to see the tickets in a ticket bag
    path('bag/summary/', ticket_bag_summary, name='ticket_bag_summary'),
]
