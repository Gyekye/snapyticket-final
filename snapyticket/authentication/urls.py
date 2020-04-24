from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from .views import RegisterView,LoginView,ProfileView,ActivateAcccountView

app_name = 'auth'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='user_register'),
    path('activate/<uidb64>/<token>/',ActivateAcccountView.as_view(),name='activate'),
    path('login/',LoginView.as_view(template_name='auth/login.html'),name='user_login'),
    path('user/profile',ProfileView.as_view(),name='user_profile'),
    path('logout/',LogoutView.as_view(template_name="auth/logout.html"),name='user_logout'),
]
