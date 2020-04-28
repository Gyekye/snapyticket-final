from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import RegisterView,LoginView,ActivateAcccountView,PasswordResetView

app_name = 'auth'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='user_register'),
    path('activate/<uidb64>/<token>/',ActivateAcccountView.as_view(),name='activate'),
    path('login/',LoginView.as_view(),name='user_login'),
    path('logout/',auth_views.LogoutView.as_view(template_name="auth/logout.html"),name='user_logout'), 
    
    # Password Reset Urls
    path('password/reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('auth:password_reset_complete')),name='password_reset_confirm'),
    path('password/reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')
]
