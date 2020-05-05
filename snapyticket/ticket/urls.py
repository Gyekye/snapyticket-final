from django.urls import path
from .views import TicketDetailView,TicketView

app_name = 'ticket'

urlpatterns = [
    path('',TicketView.as_view(),name='tickets'),
    path('detail/<slug:slug>/',TicketDetailView.as_view(),name='detail'),
]
