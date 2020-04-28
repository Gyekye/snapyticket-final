from django.shortcuts import redirect, render
from django.views.generic import View,FormView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model, update_session_auth_hash
from authentication.forms import UserChangeForm
from django.urls import reverse_lazy
from django.http import request
from django.contrib import messages
User = get_user_model()
# Create your views here.

class ProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'profile/profile.html')


class ProfileChangeView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = UserChangeForm(instance=request.user)
        context = {'form':form,}
        return render(self.request,'profile/update.html',context)

    def post(self, request, *args, **kwargs):
        form = UserChangeForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            user_phone = form.cleaned_data.get('phone')
            if len(user_phone) > 10:
                messages.info(request,'Phone number must be 10 digits')
                return redirect('profile:update')
            form.save()
            messages.success(request,'You have update your profile')
            update_session_auth_hash(request, request.user)
            return redirect('profile:user_profile')
        context = {'form':form}
        return render(self.request,'profile/update.html',context)
