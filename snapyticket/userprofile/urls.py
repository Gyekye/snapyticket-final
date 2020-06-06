from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import ProfileView, ProfileChangeView,UserTicketsList,UserTicketsDetail,UserAllTicketsList, OrganizerRegisterView

app_name = 'profile'

urlpatterns = [
<<<<<<< HEAD
    # user profile
    path('', ProfileView.as_view(), name='user_profile'),
    # url to user's orders
    path('ticket/bags/',UserTicketsList.as_view(),name='user_bags'),
    # url to user order details --- tickets
    path('ticket/bag/details/<order_ref_code>/',UserTicketsDetail.as_view(),name='bag-detail'),
    # url to all user tickets
    path('tickets/all', UserAllTicketsList.as_view(), name='all_user_tickets'),
    # url to change user profile details
    path('change/profile/details/', ProfileChangeView.as_view(), name='update'),
    
    # url for becoming an organizer
    path('organizer/register/', OrganizerRegisterView.as_view(), name='organizer-register'),

    # Password Change Views
=======
    #* url pattern to display the profile page 
    path('', ProfileView.as_view(), name='user_profile'),
    
    #* url pattern to display users ticket bag
    path('ticket/bags/',UserTicketsList.as_view(),name='user_bags'),
    
    #* url pattern to get the details of a partiular ticket bag order
    path('ticket/bag/details/<order_ref_code>/',UserTicketsDetail.as_view(),name='bag-detail'),
    
    #* url pattern to display all user tickets
    path('tickets/all', UserAllTicketsList.as_view(), name='all_user_tickets'),
    
    #* url pattern to change the details of the users profile
    path('change/profile/details/', ProfileChangeView.as_view(), name='update'),
    
    #? Password Change Views
>>>>>>> e512c0d60ac150abb816473147bb5394d1c41280
    # Todo add a message to the user after password change successful
    #* url pattern to change a users password 
    path('password/change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('auth:user_logout'), template_name='profile/password_change.html'),
         name='password_change'),
    #* url pattern to display password change down page
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
