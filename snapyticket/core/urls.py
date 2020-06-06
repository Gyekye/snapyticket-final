from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import IndexView, HomeView,PaymentView,payment_sucessful,FailedView, AllOrganizersView

app_name = 'core'

urlpatterns = [
    #* url to display index page 
    path('', IndexView.as_view(), name='index'),
    
    #* url to display the home page 
    path('home/', HomeView.as_view(), name='home'),
    
    # url to view all organizers
    path('organizer/all/', AllOrganizersView.as_view(), name='organizers'),

    #* url to display the payment page
    path('payment/', PaymentView.as_view(), name='payment'),
    
    #* url to display payment successful page takes in the order id 
    path('payment/success/<str:order_id>', payment_sucessful, name='payment_sucessful'),
    
    #* url to display a payment failed page 
    path('payment/failed/', FailedView.as_view(), name='failed_payment'),
]
