from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import IndexView, HomeView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
]
