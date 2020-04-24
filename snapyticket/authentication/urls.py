from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView,LoginView,ProfileView

app_name = 'auth'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='user_register'),
    path('login/',LoginView.as_view(),name='user_login'),
    path('user/profile',ProfileView.as_view(),name='user_profile'),
    path('logout/',LogoutView.as_view(template_name="auth/logout.html"),name='user_logout'),
]
