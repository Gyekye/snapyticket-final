from django.urls import path
from .views import DashBoardView,OrganizerUpdate,RegisterOrganizerView, OrganizerEventsView, EventSales, TrackEventSales, RequestPaymentView

app_name = 'organizer'

urlpatterns = [
    #* Url pattern to register user as organizer
    path('register/',RegisterOrganizerView.as_view(),name='register'),
    
    #* url pattern tosee the dashboard of the organizer
    path('',DashBoardView.as_view(),name='dashboard'),
    
    #* url pattern to allow users to update their organizer details
    path('update/<int:pk>/',OrganizerUpdate.as_view(),name='update'),

    #* url for organizer to select an event to track
    path('events/', OrganizerEventsView.as_view(), name='events'),

    #* url to view sales of selected event
    path('event/sales/<slug:slug>/', EventSales.as_view(), name='sales'),

    #* url to track selected event
    path('event/track/<slug:slug>/', TrackEventSales.as_view(), name='track'),

    #* url to request payment for an event
    path('event/request/payment/<slug:slug>/', RequestPaymentView.as_view(), name='request-payment'),

]
