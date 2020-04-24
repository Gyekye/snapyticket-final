from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import View,FormView,TemplateView
from django.contrib.auth.views import LoginView
from .forms import UserCreationForm
# Create your views here.


class RegisterView(View):
    def get(self,*args, **kwargs):
        form = UserCreationForm()
        context = {
            'form':form,
        }
        return render(self.request,'auth/signup.html',context)

    def post(self,*args, **kwargs):
        form = UserCreationForm(self.request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            messages.success(self.request,"You have successfully registered.Confirm your email to log in")
            self.request.user.is_active = False
            print(self.request.user.is_active)
            form.save()
            return redirect('auth:user_login')
        context = {
            'form':form,
        }
        return render(self.request,'auth/signup.html',context)
    

class LoginView(LoginView):
    template_name = 'auth/login.html'

    
class ProfileView(TemplateView):
    template_name = 'profile/profile.html'