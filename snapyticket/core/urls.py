from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import IndexView, HomeView,PaymentView,payment_sucessful,FailedView, AllOrganizersView

app_name = 'core'

urlpatterns = [
<<<<<<< HEAD
    # Index page
    path('', IndexView.as_view(), name='index'),
    # Home page -- Explore
    path('home/', HomeView.as_view(), name='home'),

    # url to view all organizers
    path('organizers/all/', AllOrganizersView.as_view(), name='organizers'),

    # Payment url
    path('payment/', PaymentView.as_view(), name='payment'),
    # Url for a sucessfull payment
    path('payment/success/<str:order_id>', payment_sucessful, name='payment_sucessful'),
    # Url for a failed payment
=======
    #* url to display index page 
    path('', IndexView.as_view(), name='index'),
    
    #* url to display the home page 
    path('home/', HomeView.as_view(), name='home'),
    
    #* url to display the payment page
    path('payment/', PaymentView.as_view(), name='payment'),
    
    #* url to display payment successful page takes in the order id 
    path('payment/success/<str:order_id>', payment_sucessful, name='payment_sucessful'),
    
    #* url to display a payment failed page 
>>>>>>> e512c0d60ac150abb816473147bb5394d1c41280
    path('payment/failed/', FailedView.as_view(), name='failed_payment'),
]
