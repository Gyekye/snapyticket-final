from django.urls import path
from .views import TicketDetail, TicketView, add_to_cart, remove_from_cart, UpdateTicketItem, ticket_bag_summary

app_name = 'ticket'

urlpatterns = [
    path('', TicketView.as_view(), name='tickets'),
    path('detail/<slug:slug>/', TicketDetail.as_view(), name='detail'),
    path('<slug:slug>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('<slug:slug>/<int:pk>/remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('<slug:slug>/<int:pk>/update_ticket_item/', UpdateTicketItem.as_view(), name='update_ticket_item'),
    path('bag/summary/', ticket_bag_summary, name='ticket_bag_summary'),
]
