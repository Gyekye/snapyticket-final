from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import IndexView, HomeView,PaymentView,payment_sucessful,FailedView, AllOrganizersView

app_name = 'core'

urlpatterns = [
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
    path('payment/failed/', FailedView.as_view(), name='failed_payment'),
]
