from django.urls import path
from .views import DashBoardView,OrganizerUpdate,RegisterOrganizer

app_name = 'organizer'

urlpatterns = [
    #* Url pattern to register user as organizer
    path('register/',RegisterOrganizer.as_view(),name='register'),
    
    #* url pattern tosee the dashboard of the organizer
    path('',DashBoardView.as_view(),name='dashboard'),
    
    #* url pattern to allow users to update their organizer details
    path('update/<int:pk>/',OrganizerUpdate.as_view(),name='update'),
]
