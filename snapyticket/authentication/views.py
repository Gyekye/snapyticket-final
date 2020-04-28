from django.shortcuts import redirect, render, resolve_url
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm 

from .forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Email Configuration imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .utils import account_activation_token
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.http.response import HttpResponse, HttpResponseRedirect
# Password Reset Imports
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.db.models import ObjectDoesNotExist
User = get_user_model()


class RegisterView(View):
    def get(self, *args, **kwargs):
        """ Redirects users back to profile when they try to access signup page
            while they are logged in
        """
        # Todo Make sure to write a redirect for event organizers too
        if self.request.user.is_authenticated:
            return redirect('profile:user_profile')
        form = UserCreationForm()
        context = {'form': form, }
        return render(self.request, 'auth/signup.html', context)

    def post(self, request, *args, **kwargs):
        # Creates an instance of the form
        form = UserCreationForm(request.POST)
        # Checks if the form is valid
        if form.is_valid():
            user_phone = form.cleaned_data.get('phone')
            if User.objects.filter(phone=user_phone).exists():
                messages.info(request,"Your phone number exists change it ")
                return redirect('auth:user_register')
            
            user_email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            use_https=False
            mail_body = render_to_string('email_snippets/account_activate/account_activate.html',
                                        {
                                            # Variables that will be passed to the template
                                            'user': user,
                                            'domain': current_site.domain,
                                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token': account_activation_token.make_token(user),
                                            'protocol':'http' if use_https else 'http',
                                        }
                                        )
            # TODO Integrate Email Sending with SendGrid to speed things up when going into production

            # Sends a Verification link to user so they can activate their account
            send_mail(mail_subject, mail_body, settings.EMAIL_HOST_USER, [user_email])
            messages.success(request,
                            "A confirmation link has been sent to your email use that to activate your account")
            return redirect('auth:user_login')
        context = {'form': form}
        return render(self.request, 'auth/signup.html', context)


class ActivateAcccountView(View):
    def get(self, request, uidb64, token):
        try:
            # Decodes the uid sent in the verification link
            uid = force_text(urlsafe_base64_decode(uidb64))
            # Gets user with Pk as uid 
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # Logins In user and redirects back to the Profile page
            login(request, user)
            messages.success(request, "Welcome to your profile")
            return redirect('profile:user_profile')
        return render(request, "email_snippets/account_activate/account_activate_failed.html")


class LoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        """ Gets the success url which is the Login redirect url"""
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get(self, *args, **kwargs):
        """ Redirects users back to profile when they try to access login page
            while they are logged in
        """
        # Todo Make sure to write a redirect for event organizers too
        if self.request.user.is_authenticated:
            return redirect('profile:user_profile')
            # This renders the login form for the user if he is not logged in
        form = self.form_class
        return render(self.request, 'auth/login.html', {'form': form})

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """
    Handle POST requests: instantiate a form instance with the passed
    POST variables and then check if it's valid.
    """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

class PasswordResetView(PasswordResetView):
    template_name = 'password/reset_form.html'
    email_template_name = 'email_snippets/password/reset_done_email.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('auth:password_reset_done') 
    
    def get(self,*args, **kwargs):
        # Todo Make sure to write a redirect for event organizers too
        if self.request.user.is_authenticated:
            return redirect('profile:user_profile')
        form = self.get_form_class()
        return render(self.request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user_email = User.objects.get(email=email)
            except ObjectDoesNotExist:
                messages.warning(request,'You email does not belong to any account ')
                return redirect('auth:user_login')
            return self.form_valid(form)
        return self.form_invalid(form)


