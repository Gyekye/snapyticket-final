from django.shortcuts import redirect,render
from django.contrib import messages
from django.views.generic import View,FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


#Email Configuration imports 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .utils import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth import login
from django.http.response import HttpResponse


class RegisterView(View):
    def get(self,*args, **kwargs):
        form = UserCreationForm()
        context = {'form':form,}
        return render(self.request,'auth/signup.html',context)
    
    def post(self,request,*args, **kwargs):
        #Creates an instance of the form
        form = UserCreationForm(request.POST)
        #Checks if the form is valid 
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            mail_body = render_to_string('email_snippets/account_activate/account_activate.html',
            {
                    #Variables that will be passed to the template
                    'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
            }
            )
            user.email_user(mail_subject,mail_body)
            return redirect('auth:user_login')
            messages.success(request,"A confirmation link has been sent to your email use that to activate your account")
        context = {'form':form} 
        return render(self.request,'auth/signup.html',context)
    
    
class ActivateAcccountView(View):   
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user,token):
            user.is_active = True
            user.save()
            login(request,user)
            return redirect('auth:user_profile')
            messages.success(request,'You have successfully activated your account')
        else:
            return render(request,"email_snippets/account_activate/account_activate_failed.html")
        
        
class ProfileView(LoginRequiredMixin,View):
        def get(self,*args, **kwargs):
            return render(self.request,'profile/profile.html')