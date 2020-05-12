from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import IndexView, HomeView,PaymentView,SuccessView,FailedView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/success/', SuccessView.as_view(), name='success_payment'),
    path('payment/failed/', FailedView.as_view(), name='failed_payment'),
]
