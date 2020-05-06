from django.urls import path
from .views import TicketDetail,TicketView,_add_to_cart,_remove_from_cart

app_name = 'ticket'

urlpatterns = [
    path('',TicketView.as_view(),name='tickets'),
    path('detail/<slug:slug>/',TicketDetail.as_view(),name='detail'),
    path('detail/<slug:slug>/add_to_cart/',_add_to_cart,name='add_to_cart'),
    path('detail/<slug:slug>/<int:pk>/remove_from_cart/',_remove_from_cart,name='remove_from_cart'),
]
