from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import ProfileView,ProfileChangeView

app_name = 'profile'

urlpatterns = [
    path('',ProfileView.as_view(),name='user_profile'),
    path('change/details/',ProfileChangeView.as_view(),name='update'),
    # Password Change Views
    #Todo add a message to the user after pasword change successful 
    path('password/change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('auth:user_logout')),name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
