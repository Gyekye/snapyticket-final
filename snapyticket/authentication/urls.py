from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import RegisterView,LoginView,ActivateAcccountView,PasswordResetView

app_name = 'auth'

urlpatterns = [
    #* url pattern to register user 
    path('register/',RegisterView.as_view(),name='user_register'),
    
    #* url patttern to send user an activation link to their email
    path('activate/<uidb64>/<token>/',ActivateAcccountView.as_view(),name='activate'),
    
    #* url pattern to log users in
    path('login/',LoginView.as_view(),name='user_login'),
    
    #* url pattern to log users out 
    path('logout/',auth_views.LogoutView.as_view(template_name="auth/logout.html"),name='user_logout'), 
    
    #? Password Reset Urls
    #* url pattern to reset pasword
    path('password/reset/',PasswordResetView.as_view(),name='password_reset'),
    #* url pattern to send the password reset email
    path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password/reset_done.html'),name='password_reset_done'),
    #* url pattern to send the password reset link 
    path('password/reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('auth:password_reset_complete'), template_name='password/reset_confirm.html'),name='password_reset_confirm'),
    #* url pattern to display a password reset down page to user
    path('password/reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password/reset_complete.html'),name='password_reset_complete'),

]
